import { useState, useCallback } from 'react';
import api from '@/lib/api';
import { Patient, PaginatedResponse } from '@/types';
import toast from 'react-hot-toast';

export function usePatients() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [total, setTotal] = useState(0);
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
      setError(err.message || 'Failed to fetch patients');
      toast.error('Failed to fetch patients');
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
      toast.error(err.response?.data?.detail || 'Failed to create patient');
      throw err;
    }
  };

  const updatePatient = async (id: string, patientData: Partial<Patient>) => {
    try {
      const { data } = await api.put<Patient>(`/api/patients/${id}`, patientData);
      setPatients(prev => prev.map(p => p.id === id ? data : p));
      toast.success('Patient updated successfully');
      return data;
    } catch (err: any) {
      toast.error(err.response?.data?.detail || 'Failed to update patient');
      throw err;
    }
  };

  const deletePatient = async (id: string) => {
    try {
      await api.delete(`/api/patients/${id}`);
      setPatients(prev => prev.filter(p => p.id !== id));
      toast.success('Patient deleted successfully');
    } catch (err: any) {
      toast.error('Failed to delete patient');
      throw err;
    }
  };

  return { patients, total, loading, error, fetchPatients, createPatient, updatePatient, deletePatient };
}
