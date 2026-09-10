import { useState, useCallback } from 'react';
import api from '@/lib/api';
import { Appointment, PaginatedResponse } from '@/types';
import toast from 'react-hot-toast';

export function useAppointments() {
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [total, setTotal] = useState(0);
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
      setError(err.message || 'Failed to fetch appointments');
      toast.error('Failed to fetch appointments');
    } finally {
      setLoading(false);
    }
  }, []);

  const createAppointment = async (appointmentData: Partial<Appointment>) => {
    try {
      const { data } = await api.post<Appointment>('/api/appointments', appointmentData);
      toast.success('Appointment created successfully');
      return data;
    } catch (err: any) {
      toast.error(err.response?.data?.detail || 'Failed to create appointment');
      throw err;
    }
  };

  const updateAppointment = async (id: string, appointmentData: Partial<Appointment>) => {
    try {
      const { data } = await api.put<Appointment>(`/api/appointments/${id}`, appointmentData);
      setAppointments(prev => prev.map(a => a.id === id ? data : a));
      toast.success('Appointment updated successfully');
      return data;
    } catch (err: any) {
      toast.error(err.response?.data?.detail || 'Failed to update appointment');
      throw err;
    }
  };

  const deleteAppointment = async (id: string) => {
    try {
      await api.delete(`/api/appointments/${id}`);
      setAppointments(prev => prev.filter(a => a.id !== id));
      toast.success('Appointment deleted successfully');
    } catch (err: any) {
      toast.error('Failed to delete appointment');
      throw err;
    }
  };

  return { appointments, total, loading, error, fetchAppointments, createAppointment, updateAppointment, deleteAppointment };
}
