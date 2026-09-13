"use client";

import React, { useState, useEffect } from "react";
import { format, addDays, subDays } from "date-fns";
import { ChevronLeft, ChevronRight, Clock, Plus, CheckCircle, Calendar as CalendarIcon } from "lucide-react";
import { PageWrapper } from "@/components/layout/PageWrapper";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";
import { Select } from "@/components/ui/Select";
import { useAppointments } from "@/hooks/useAppointments";
import { usePatients } from "@/hooks/usePatients";
import api from "@/lib/api";
import { getStatusColor, formatTime } from "@/lib/utils";
import { Appointment, User } from "@/types";
import toast from "react-hot-toast";

export default function AppointmentsPage() {
  const [date, setDate] = useState(new Date());
  const formattedDate = format(date, "yyyy-MM-dd");
  const { appointments, loading, fetchAppointments, createAppointment } = useAppointments();
  const { patients, fetchPatients } = usePatients();
  
  const [dentists, setDentists] = useState<User[]>([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState<{
    patient_id: string;
    dentist_id: string;
    date: string;
    start_time: string;
    duration_minutes: number;
    status: string;
    appointment_type: string;
    notes?: string;
  }>({
    patient_id: "",
    dentist_id: "",
    date: formattedDate,
    start_time: "09:00",
    duration_minutes: 30,
    status: "confirmed",
    appointment_type: "Consultation",
    notes: "",
  });
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    fetchAppointments(formattedDate);
    fetchPatients(1, 100);
    
    const fetchDentists = async () => {
      try {
        const { data } = await api.get("/api/users/dentists");
        setDentists(data.items || data || []);
        if (data.length > 0 && !formData.dentist_id) {
          setFormData((prev) => ({ ...prev, dentist_id: data[0].id }));
        }
      } catch (err) {
        console.error("Failed to load dentists", err);
      }
    };
    fetchDentists();
  }, [fetchAppointments, fetchPatients, formattedDate]);

  const handlePrevDay = () => setDate(subDays(date, 1));
  const handleNextDay = () => setDate(addDays(date, 1));
  const handleToday = () => setDate(new Date());

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.patient_id) {
      toast.error("Please select a patient");
      return;
    }
    if (!formData.dentist_id) {
      toast.error("Please select a dentist");
      return;
    }
    setIsSubmitting(true);
    try {
      await createAppointment({
        ...formData,
        date: formData.date || formattedDate,
      } as any);
      setIsModalOpen(false);
      fetchAppointments(formattedDate);
    } catch (err: any) {
      // Handled in hook
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleCheckIn = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      await api.post(`/api/appointments/${id}/check-in`);
      toast.success("Patient checked in!");
      fetchAppointments(formattedDate);
    } catch (err) {
      toast.error("Failed to check in");
    }
  };

  const patientOptions = patients.map((p) => ({
    label: `${p.full_name} (${p.patient_id_display}) - ${p.phone}`,
    value: p.id,
  }));

  const dentistOptions = dentists.map((d) => ({
    label: `${d.full_name} (${d.specialization || "Dentist"})`,
    value: d.id,
  }));

  return (
    <PageWrapper
      title="Appointments"
      action={
        <Button onClick={() => setIsModalOpen(true)} className="bg-primary text-white">
          + New appointment
        </Button>
      }
    >
      <div className="flex flex-col sm:flex-row items-center justify-between mb-6 bg-white p-4 rounded-lg shadow-sm border border-gray-200 gap-4">
        <div className="flex items-center space-x-2">
          <Button variant="outline" size="sm" onClick={handlePrevDay}>
            <ChevronLeft className="h-4 w-4" />
          </Button>
          <Button variant="outline" size="sm" onClick={handleToday}>
            Today
          </Button>
          <Button variant="outline" size="sm" onClick={handleNextDay}>
            <ChevronRight className="h-4 w-4" />
          </Button>
        </div>
        <div className="flex items-center gap-2 font-bold text-lg text-gray-900">
          <CalendarIcon className="w-5 h-5 text-primary" />
          {format(date, "EEEE, MMMM d, yyyy")}
        </div>
      </div>

      {loading ? (
        <LoadingSpinner />
      ) : appointments.length > 0 ? (
        <div className="space-y-3">
          {appointments.map((apt) => (
            <Card
              key={apt.id}
              className="p-4 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 hover:border-primary transition-colors border-gray-200"
            >
              <div className="flex items-center gap-4">
                <div className="p-3 bg-blue-50 text-primary rounded-lg flex items-center justify-center">
                  <Clock className="w-6 h-6" />
                </div>
                <div>
                  <div className="text-base font-bold text-gray-900 flex items-center gap-2">
                    {formatTime(apt.start_time)} - {formatTime(apt.end_time)}
                    <span className="text-xs font-normal text-gray-500">({apt.duration_minutes} min)</span>
                  </div>
                  <div className="text-base font-medium text-gray-900 mt-0.5">{apt.patient_name}</div>
                  <div className="text-xs text-gray-500 mt-0.5">
                    {apt.appointment_type} • Dr. {apt.dentist_name}
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-3 self-end md:self-center">
                {apt.status === "confirmed" && (
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={(e) => handleCheckIn(apt.id, e)}
                    className="flex items-center gap-1.5 text-xs text-emerald-700 border-emerald-300 hover:bg-emerald-50"
                  >
                    <CheckCircle className="w-3.5 h-3.5" /> Check-in
                  </Button>
                )}
                <Badge className={getStatusColor(apt.status)}>{apt.status}</Badge>
              </div>
            </Card>
          ))}
        </div>
      ) : (
        <Card className="p-12 text-center text-gray-500">
          No appointments scheduled for {format(date, "MMMM d, yyyy")}.
        </Card>
      )}

      {/* New Appointment Modal */}
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="New Appointment">
        <form onSubmit={handleSubmit} className="space-y-4">
          <Select
            label="Patient"
            required
            placeholder="Select patient..."
            value={formData.patient_id}
            onChange={(e) => setFormData({ ...formData, patient_id: e.target.value })}
            options={patientOptions}
          />

          <Select
            label="Doctor / Dentist"
            required
            placeholder="Select doctor..."
            value={formData.dentist_id}
            onChange={(e) => setFormData({ ...formData, dentist_id: e.target.value })}
            options={dentistOptions}
          />

          <div className="grid grid-cols-2 gap-4">
            <Input
              type="date"
              label="Date"
              required
              value={formData.date}
              onChange={(e) => setFormData({ ...formData, date: e.target.value })}
            />
            <Input
              type="time"
              label="Start Time"
              required
              value={formData.start_time}
              onChange={(e) => setFormData({ ...formData, start_time: e.target.value })}
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <Input
              type="number"
              label="Duration (min)"
              required
              min={10}
              step={5}
              value={formData.duration_minutes}
              onChange={(e) => setFormData({ ...formData, duration_minutes: parseInt(e.target.value) || 30 })}
            />
            <Select
              label="Status"
              required
              value={formData.status}
              onChange={(e) => setFormData({ ...formData, status: e.target.value })}
              options={[
                { label: "Confirmed", value: "confirmed" },
                { label: "Pending", value: "pending" },
                { label: "Cancelled", value: "cancelled" },
              ]}
            />
          </div>

          <Select
            label="Type of visit"
            required
            value={formData.appointment_type}
            onChange={(e) => setFormData({ ...formData, appointment_type: e.target.value })}
            options={[
              { label: "Consultation", value: "Consultation" },
              { label: "Cleaning & Scaling", value: "Cleaning" },
              { label: "Filling", value: "Filling" },
              { label: "Root Canal", value: "Root Canal" },
              { label: "Crown & Bridge", value: "Crown" },
              { label: "Tooth Extraction", value: "Extraction" },
              { label: "Follow-up", value: "Follow-up" },
              { label: "Emergency", value: "Emergency" },
            ]}
          />

          <Input
            label="Notes / Reason for visit"
            placeholder="e.g. Toothache lower molar"
            value={formData.notes || ""}
            onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
          />

          <div className="flex justify-end gap-3 pt-4 border-t">
            <Button variant="outline" type="button" onClick={() => setIsModalOpen(false)}>
              Cancel
            </Button>
            <Button type="submit" isLoading={isSubmitting} className="bg-primary text-white">
              Save appointment
            </Button>
          </div>
        </form>
      </Modal>
    </PageWrapper>
  );
}
