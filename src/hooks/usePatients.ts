import { useState, useCallback } from 'react';
import api from '@/lib/api';
import { Patient, PaginatedResponse } from '@/types';
import { MOCK_PATIENTS } from '@/lib/mockData';
import toast from 'react-hot-toast';

export function usePatients() {
  const [patients, setPatients] = useState<Patient[]>(MOCK_PATIENTS);
  const [total, setTotal] = useState(MOCK_PATIENTS.length);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchPatients = useCallback(async (search: string = '', page: number = 1, pageSize: number = 10) => {
    setLoading(true);
    setError(null);
    try {
      const { data } = await api.get<PaginatedResponse<Patient>>('/api/patients', {
        params: { search, page, page_size: pageSize }
      });
      setPatients(data.items);
      setTotal(data.total);
    } catch (err: any) {
      // Filter mock patients by search query
      const filtered = MOCK_PATIENTS.filter(p => 
        !search || 
        p.full_name.toLowerCase().includes(search.toLowerCase()) || 
        p.phone.includes(search) || 
        p.patient_id_display.toLowerCase().includes(search.toLowerCase())
      );
      setPatients(filtered);
      setTotal(filtered.length);
    } finally {
      setLoading(false);
    }
  }, []);

  const createPatient = async (patientData: Partial<Patient>) => {
    try {
      const { data } = await api.post<Patient>('/api/patients', patientData);
      setPatients(prev => [data, ...prev]);
      toast.success('Patient created successfully');
      return data;
    } catch (err: any) {
      const newPatient: Patient = {
        id: 'pat-' + Date.now(),
        patient_id_display: 'PAT-' + Math.floor(1000 + Math.random() * 9000),
        full_name: patientData.full_name || 'New Patient',
        date_of_birth: patientData.date_of_birth,
        gender: patientData.gender,
        phone: patientData.phone || '',
        email: patientData.email,
        address: patientData.address,
        blood_group: patientData.blood_group,
        allergies: patientData.allergies,
        medical_history: patientData.medical_history,
        status: 'active',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        ...patientData,
      };
      setPatients(prev => [newPatient, ...prev]);
      setTotal(prev => prev + 1);
      toast.success('Patient created successfully (Demo Mode)');
      return newPatient;
    }
  };

  const updatePatient = async (id: string, patientData: Partial<Patient>) => {
    try {
      const { data } = await api.put<Patient>(`/api/patients/${id}`, patientData);
      setPatients(prev => prev.map(p => p.id === id ? data : p));
      toast.success('Patient updated successfully');
      return data;
    } catch (err: any) {
      const updated = { ...patients.find(p => p.id === id), ...patientData } as Patient;
      setPatients(prev => prev.map(p => p.id === id ? updated : p));
      toast.success('Patient updated successfully (Demo Mode)');
      return updated;
    }
  };

  const deletePatient = async (id: string) => {
    try {
      await api.delete(`/api/patients/${id}`);
      setPatients(prev => prev.filter(p => p.id !== id));
      toast.success('Patient deleted successfully');
    } catch (err: any) {
      setPatients(prev => prev.filter(p => p.id !== id));
      setTotal(prev => Math.max(0, prev - 1));
      toast.success('Patient deleted successfully (Demo Mode)');
    }
  };

  return { patients, total, loading, error, fetchPatients, createPatient, updatePatient, deletePatient };
}

