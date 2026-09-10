import { useState, useCallback } from 'react';
import api from '@/lib/api';
import { DashboardStats, TodaySchedule } from '@/types';
import toast from 'react-hot-toast';

export function useDashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [schedule, setSchedule] = useState<TodaySchedule[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchDashboardData = useCallback(async () => {
    setLoading(true);
    try {
      const [statsRes, scheduleRes] = await Promise.all([
        api.get<DashboardStats>('/api/dashboard/stats'),
        api.get<TodaySchedule[]>('/api/dashboard/today-schedule')
      ]);
      setStats(statsRes.data);
      setSchedule(scheduleRes.data);
    } catch (err) {
      toast.error('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  }, []);

  return { stats, schedule, loading, fetchDashboardData };
}
