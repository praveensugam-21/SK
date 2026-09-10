"use client";

import React, { useEffect } from "react";
import { Users, Calendar as CalendarIcon, IndianRupee, TrendingUp } from "lucide-react";
import { PageWrapper } from "@/components/layout/PageWrapper";
import { StatsCard } from "@/components/ui/StatsCard";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { useDashboard } from "@/hooks/useDashboard";
import { formatCurrency, getStatusColor } from "@/lib/utils";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts';

export default function DashboardPage() {
  const { stats, schedule, loading, fetchDashboardData } = useDashboard();

  useEffect(() => {
    fetchDashboardData();
  }, [fetchDashboardData]);

  if (loading || !stats) {
    return <PageWrapper title="Dashboard"><LoadingSpinner /></PageWrapper>;
  }

  // Mock data for charts since it's not provided by API
  const weeklyData = [
    { name: 'Mon', appointments: 4 },
    { name: 'Tue', appointments: 7 },
    { name: 'Wed', appointments: 5 },
    { name: 'Thu', appointments: 8 },
    { name: 'Fri', appointments: 6 },
    { name: 'Sat', appointments: 9 },
    { name: 'Sun', appointments: 2 },
  ];

  const revenueData = [
    { name: 'Week 1', revenue: 15000 },
    { name: 'Week 2', revenue: 22000 },
    { name: 'Week 3', revenue: 18000 },
    { name: 'Week 4', revenue: 28000 },
  ];

  return (
    <PageWrapper title="Dashboard">
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
        <StatsCard title="Total Patients" value={stats.total_patients} icon={<Users />} />
        <StatsCard title="Today's Appointments" value={stats.todays_appointments} icon={<CalendarIcon />} />
        <StatsCard title="Collected Today" value={formatCurrency(stats.todays_revenue)} icon={<IndianRupee />} />
        <StatsCard title="Outstanding" value={formatCurrency(stats.outstanding_amount)} icon={<TrendingUp />} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
        <Card className="lg:col-span-2 p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Weekly Appointments</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={weeklyData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="name" axisLine={false} tickLine={false} />
                <YAxis axisLine={false} tickLine={false} />
                <Tooltip cursor={{fill: 'transparent'}} />
                <Bar dataKey="appointments" fill="#3b82f6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>

        <Card className="p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Revenue Trend</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={revenueData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="name" axisLine={false} tickLine={false} />
                <YAxis axisLine={false} tickLine={false} tickFormatter={(val) => `₹${val/1000}k`} />
                <Tooltip />
                <Line type="monotone" dataKey="revenue" stroke="#3b82f6" strokeWidth={3} dot={{r: 4}} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>

      <Card className="p-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">Today's Schedule</h2>
        {schedule.length > 0 ? (
          <div className="space-y-4">
            {schedule.map((apt) => (
              <div key={apt.appointment_id} className="flex items-center justify-between p-4 border border-gray-100 rounded-lg bg-gray-50">
                <div className="flex items-center gap-4">
                  <div className="font-medium text-gray-900 w-24">{apt.time}</div>
                  <div>
                    <div className="font-medium text-gray-900">{apt.patient_name}</div>
                    <div className="text-sm text-gray-500">{apt.type} • {apt.duration} min</div>
                  </div>
                </div>
                <Badge className={getStatusColor(apt.status)}>{apt.status}</Badge>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500">No appointments scheduled for today.</p>
        )}
      </Card>
    </PageWrapper>
  );
}
