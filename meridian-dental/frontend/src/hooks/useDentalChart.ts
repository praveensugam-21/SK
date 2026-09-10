import { useState, useCallback } from 'react';
import api from '@/lib/api';
import { ToothRecord } from '@/types';
import toast from 'react-hot-toast';

export function useDentalChart(patientId: string) {
  const [records, setRecords] = useState<ToothRecord[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchChart = useCallback(async () => {
    if (!patientId) return;
    setLoading(true);
    try {
      const { data } = await api.get<any>(`/api/patients/${patientId}/dental-chart`);
      const teethList = Array.isArray(data) ? data : (data?.teeth || []);
      setRecords(teethList);
    } catch (err) {
      toast.error('Failed to load dental chart');
      setRecords([]);
    } finally {
      setLoading(false);
    }
  }, [patientId]);

  const updateTooth = async (toothNumber: number, data: Partial<ToothRecord>) => {
    try {
      const { data: updated } = await api.put<ToothRecord>(`/api/patients/${patientId}/teeth/${toothNumber}`, data);
      setRecords(prev => {
        const arr = Array.isArray(prev) ? prev : [];
        const idx = arr.findIndex(r => r.tooth_number === toothNumber);
        if (idx >= 0) {
          const newRecords = [...arr];
          newRecords[idx] = updated;
          return newRecords;
        }
        return [...arr, updated];
      });
      toast.success(`Tooth ${toothNumber} set to ${data.condition}`);
    } catch (err) {
      toast.error(`Failed to update tooth ${toothNumber}`);
      throw err;
    }
  };

  return { records, loading, fetchChart, updateTooth };
}
