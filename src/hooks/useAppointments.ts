import { useState, useCallback } from 'react';
import api from '@/lib/api';
import { Appointment, PaginatedResponse } from '@/types';
import { MOCK_APPOINTMENTS } from '@/lib/mockData';
import toast from 'react-hot-toast';

export function useAppointments() {
  const [appointments, setAppointments] = useState<Appointment[]>(MOCK_APPOINTMENTS);
  const [total, setTotal] = useState(MOCK_APPOINTMENTS.length);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchAppointments = useCallback(async (date?: string, page: number = 1, pageSize: number = 20) => {
    setLoading(true);
    setError(null);
    try {
      const params: any = { page, page_size: pageSize };
      if (date) params.date = date;
      const { data } = await api.get<PaginatedResponse<Appointment>>('/api/appointments', { params });
      setAppointments(data.items);
      setTotal(data.total);
    } catch (err: any) {
      const filtered = date 
        ? MOCK_APPOINTMENTS.filter(a => a.date === date) 
        : MOCK_APPOINTMENTS;
      setAppointments(filtered);
      setTotal(filtered.length);
    } finally {
      setLoading(false);
    }
  }, []);

  const createAppointment = async (appointmentData: Partial<Appointment>) => {
    try {
      const { data } = await api.post<Appointment>('/api/appointments', appointmentData);
      setAppointments(prev => [data, ...prev]);
      toast.success('Appointment created successfully');
      return data;
    } catch (err: any) {
      const newAppt: Appointment = {
        id: 'apt-' + Date.now(),
        patient_id: appointmentData.patient_id || 'pat-01',
        dentist_id: appointmentData.dentist_id || 'usr-dentist-01',
        patient_name: appointmentData.patient_name || 'Patient',
        dentist_name: appointmentData.dentist_name || 'Dr. Arthur Meridian',
        date: appointmentData.date || new Date().toISOString().split('T')[0],
        start_time: appointmentData.start_time || '10:00',
        end_time: appointmentData.end_time || '10:30',
        duration_minutes: appointmentData.duration_minutes || 30,
        appointment_type: appointmentData.appointment_type || 'General Consultation',
        status: appointmentData.status || 'scheduled',
        notes: appointmentData.notes,
        created_at: new Date().toISOString(),
      };
      setAppointments(prev => [newAppt, ...prev]);
      setTotal(prev => prev + 1);
      toast.success('Appointment created successfully (Demo Mode)');
      return newAppt;
    }
  };

  const updateAppointment = async (id: string, appointmentData: Partial<Appointment>) => {
    try {
      const { data } = await api.put<Appointment>(`/api/appointments/${id}`, appointmentData);
      setAppointments(prev => prev.map(a => a.id === id ? data : a));
      toast.success('Appointment updated successfully');
      return data;
    } catch (err: any) {
      const updated = { ...appointments.find(a => a.id === id), ...appointmentData } as Appointment;
      setAppointments(prev => prev.map(a => a.id === id ? updated : a));
      toast.success('Appointment updated successfully (Demo Mode)');
      return updated;
    }
  };

  const deleteAppointment = async (id: string) => {
    try {
      await api.delete(`/api/appointments/${id}`);
      setAppointments(prev => prev.filter(a => a.id !== id));
      toast.success('Appointment deleted successfully');
    } catch (err: any) {
      setAppointments(prev => prev.filter(a => a.id !== id));
      setTotal(prev => Math.max(0, prev - 1));
      toast.success('Appointment deleted successfully (Demo Mode)');
    }
  };

  return { appointments, total, loading, error, fetchAppointments, createAppointment, updateAppointment, deleteAppointment };
}

