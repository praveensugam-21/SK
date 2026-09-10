"use client";

import React, { useEffect, useState, useCallback } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { PageWrapper } from "@/components/layout/PageWrapper";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Textarea } from "@/components/ui/Textarea";
import { Modal } from "@/components/ui/Modal";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import DentalChart from "@/components/dental-chart/DentalChart";
import api from "@/lib/api";
import { Patient, Note, Appointment, TreatmentPlan, Prescription, Invoice, TimelineEvent } from "@/types";
import { calculateAge, formatCurrency, formatDate, getStatusColor } from "@/lib/utils";
import toast from "react-hot-toast";
import { Calendar, FileText, Plus, Clock, Receipt, Pill, Activity, User, ShieldAlert, CheckCircle2 } from "lucide-react";

export default function PatientProfilePage() {
  const { id } = useParams() as { id: string };
  const [patient, setPatient] = useState<Patient | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("chart");

  // Tab Data states
  const [notes, setNotes] = useState<Note[]>([]);
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [treatmentPlans, setTreatmentPlans] = useState<TreatmentPlan[]>([]);
  const [prescriptions, setPrescriptions] = useState<Prescription[]>([]);
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [timeline, setTimeline] = useState<TimelineEvent[]>([]);
  const [tabLoading, setTabLoading] = useState(false);

  // Modal states
  const [showNoteModal, setShowNoteModal] = useState(false);
  const [noteContent, setNoteContent] = useState("");
  const [isClinicalNote, setIsClinicalNote] = useState(false);

  const fetchPatient = useCallback(async () => {
    try {
      const { data } = await api.get<Patient>(`/api/patients/${id}`);
      setPatient(data);
    } catch (err) {
      toast.error("Failed to load patient");
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    fetchPatient();
  }, [fetchPatient]);

  // Load tab-specific data when activeTab changes
  useEffect(() => {
    if (!id) return;
    const loadTabData = async () => {
      setTabLoading(true);
      try {
        if (activeTab === "notes") {
          const res = await api.get(`/api/notes?patient_id=${id}`);
          setNotes(res.data.items || res.data || []);
        } else if (activeTab === "appointments") {
          const res = await api.get(`/api/appointments?patient_id=${id}`);
          setAppointments(res.data.items || []);
        } else if (activeTab === "treatments") {
          const res = await api.get(`/api/treatment-plans?patient_id=${id}`);
          setTreatmentPlans(res.data.items || res.data || []);
        } else if (activeTab === "prescriptions") {
          const res = await api.get(`/api/prescriptions?patient_id=${id}`);
          setPrescriptions(res.data.items || res.data || []);
        } else if (activeTab === "invoices") {
          const res = await api.get(`/api/invoices?patient_id=${id}`);
          setInvoices(res.data.items || []);
        } else if (activeTab === "timeline") {
          const res = await api.get(`/api/patients/${id}/timeline`);
          setTimeline(res.data.items || res.data || []);
        }
      } catch (err) {
        console.error("Failed to load tab data", err);
      } finally {
        setTabLoading(false);
      }
    };
    loadTabData();
  }, [id, activeTab]);

  const handleAddNote = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!noteContent.trim()) return;
    try {
      await api.post("/api/notes", {
        patient_id: id,
        content: noteContent,
        note_type: isClinicalNote ? "clinical" : "general",
        is_clinical: isClinicalNote,
      });
      toast.success("Note added");
      setNoteContent("");
      setShowNoteModal(false);
      // Refresh notes & timeline
      const res = await api.get(`/api/notes?patient_id=${id}`);
      setNotes(res.data.items || res.data || []);
    } catch (err) {
      toast.error("Failed to add note");
    }
  };

  if (loading) return <PageWrapper><LoadingSpinner /></PageWrapper>;
  if (!patient) return <PageWrapper><div className="p-8 text-center text-gray-500">Patient not found</div></PageWrapper>;

  const tabs = [
    { id: "chart", label: "Dental Chart" },
    { id: "notes", label: "Notes" },
    { id: "appointments", label: "Appointments" },
    { id: "treatments", label: "Treatments" },
    { id: "prescriptions", label: "Prescriptions" },
    { id: "invoices", label: "Invoices" },
    { id: "timeline", label: "Timeline" },
  ];

  return (
    <PageWrapper>
      {/* Patient Header Card */}
      <Card className="p-6 mb-6 bg-white border border-gray-200">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <h1 className="text-2xl font-bold text-gray-900">{patient.full_name}</h1>
              <Badge className={patient.status === "active" ? "bg-emerald-100 text-emerald-800" : "bg-gray-100 text-gray-800"}>
                {patient.status}
              </Badge>
              {patient.blood_group && (
                <Badge className="bg-red-50 text-red-700 border border-red-200">
                  Blood Group: {patient.blood_group}
                </Badge>
              )}
            </div>
            <div className="flex flex-wrap gap-x-6 gap-y-2 text-sm text-gray-600">
              <span><strong>ID:</strong> {patient.patient_id_display}</span>
              {patient.date_of_birth && <span><strong>Age:</strong> {calculateAge(patient.date_of_birth)} yrs</span>}
              <span><strong>Phone:</strong> {patient.phone}</span>
              {patient.email && <span><strong>Email:</strong> {patient.email}</span>}
            </div>
            {patient.allergies && (
              <div className="mt-2 text-xs flex items-center gap-1.5 text-amber-700 font-medium">
                <ShieldAlert className="w-4 h-4" /> Allergies: {patient.allergies}
              </div>
            )}
          </div>
          <div className="flex items-center gap-3">
            <Link href="/appointments">
              <Button size="sm" variant="outline" className="flex items-center gap-2">
                <Calendar className="w-4 h-4" /> Book Visit
              </Button>
            </Link>
            <Link href="/billing">
              <Button size="sm" className="flex items-center gap-2 bg-primary text-white">
                <Receipt className="w-4 h-4" /> New Invoice
              </Button>
            </Link>
          </div>
        </div>
      </Card>

      {/* Tabs Navigation */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="-mb-px flex space-x-6 overflow-x-auto">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`whitespace-nowrap py-3 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === tab.id
                  ? "border-primary text-primary font-semibold"
                  : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      {/* Tab Contents */}
      <div>
        {/* Dental Chart */}
        {activeTab === "chart" && <DentalChart patientId={patient.id} />}

        {/* Notes Tab */}
        {activeTab === "notes" && (
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <h2 className="text-lg font-semibold text-gray-900">Clinical & Patient Notes</h2>
              <Button size="sm" onClick={() => setShowNoteModal(true)} className="flex items-center gap-1.5 bg-primary text-white">
                <Plus className="w-4 h-4" /> Add Note
              </Button>
            </div>

            {patient.notes && (
              <Card className="p-4 bg-amber-50 border-amber-200">
                <h3 className="text-xs font-bold uppercase tracking-wider text-amber-800 mb-1">Registration Notes</h3>
                <p className="text-sm text-amber-900">{patient.notes}</p>
              </Card>
            )}

            {tabLoading ? (
              <LoadingSpinner />
            ) : notes.length === 0 ? (
              <Card className="p-8 text-center text-gray-500">No additional clinical notes recorded yet.</Card>
            ) : (
              <div className="space-y-3">
                {notes.map((n) => (
                  <Card key={n.id} className="p-4 border-gray-200">
                    <div className="flex justify-between items-start mb-2">
                      <div className="flex items-center gap-2">
                        <Badge className={n.is_clinical ? "bg-purple-100 text-purple-800" : "bg-gray-100 text-gray-800"}>
                          {n.is_clinical ? "Clinical" : "General"}
                        </Badge>
                        <span className="text-xs text-gray-500">By {n.author_name || "Staff"}</span>
                      </div>
                      <span className="text-xs text-gray-400">{formatDate(n.created_at)}</span>
                    </div>
                    <p className="text-sm text-gray-800 whitespace-pre-wrap">{n.content}</p>
                  </Card>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Appointments Tab */}
        {activeTab === "appointments" && (
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <h2 className="text-lg font-semibold text-gray-900">Appointment History</h2>
              <Link href="/appointments">
                <Button size="sm" className="flex items-center gap-1.5 bg-primary text-white">
                  <Plus className="w-4 h-4" /> Schedule Appointment
                </Button>
              </Link>
            </div>

            {tabLoading ? (
              <LoadingSpinner />
            ) : appointments.length === 0 ? (
              <Card className="p-8 text-center text-gray-500">No appointment records found for this patient.</Card>
            ) : (
              <div className="space-y-3">
                {appointments.map((apt) => (
                  <Card key={apt.id} className="p-4 flex items-center justify-between border-gray-200">
                    <div className="flex items-center gap-4">
                      <div className="p-2.5 bg-blue-50 text-blue-700 rounded-lg">
                        <Clock className="w-5 h-5" />
                      </div>
                      <div>
                        <div className="font-semibold text-gray-900">{formatDate(apt.date)} at {apt.start_time}</div>
                        <div className="text-xs text-gray-500 capitalize">{apt.appointment_type} • {apt.duration_minutes} mins</div>
                      </div>
                    </div>
                    <Badge className={getStatusColor(apt.status)}>{apt.status}</Badge>
                  </Card>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Treatments Tab */}
        {activeTab === "treatments" && (
          <div className="space-y-4">
            <h2 className="text-lg font-semibold text-gray-900">Treatment Plans & History</h2>
            {tabLoading ? (
              <LoadingSpinner />
            ) : treatmentPlans.length === 0 ? (
              <Card className="p-8 text-center text-gray-500">No treatment plans recorded yet.</Card>
            ) : (
              <div className="space-y-4">
                {treatmentPlans.map((tp) => (
                  <Card key={tp.id} className="p-5 border-gray-200">
                    <div className="flex justify-between items-start mb-3">
                      <div>
                        <h3 className="font-bold text-gray-900 text-base">{tp.title}</h3>
                        <p className="text-xs text-gray-500">Doctor: {tp.dentist_name || "Assigned Dentist"}</p>
                      </div>
                      <Badge className={getStatusColor(tp.status)}>{tp.status}</Badge>
                    </div>
                    {tp.description && <p className="text-sm text-gray-600 mb-3">{tp.description}</p>}
                    <div className="text-sm font-semibold text-gray-900 pt-2 border-t border-gray-100 flex justify-between">
                      <span>Total Estimated Cost:</span>
                      <span>{formatCurrency(tp.total_estimated_cost)}</span>
                    </div>
                  </Card>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Prescriptions Tab */}
        {activeTab === "prescriptions" && (
          <div className="space-y-4">
            <h2 className="text-lg font-semibold text-gray-900">Prescriptions</h2>
            {tabLoading ? (
              <LoadingSpinner />
            ) : prescriptions.length === 0 ? (
              <Card className="p-8 text-center text-gray-500">No prescriptions issued yet.</Card>
            ) : (
              <div className="space-y-3">
                {prescriptions.map((p) => (
                  <Card key={p.id} className="p-4 border-gray-200">
                    <div className="flex justify-between items-start mb-2">
                      <div className="flex items-center gap-2">
                        <Pill className="w-4 h-4 text-emerald-600" />
                        <span className="font-semibold text-sm text-gray-900">{formatDate(p.date)}</span>
                        <span className="text-xs text-gray-500">by {p.dentist_name || "Doctor"}</span>
                      </div>
                    </div>
                    {p.diagnosis && <p className="text-xs text-gray-600 mb-2"><strong>Diagnosis:</strong> {p.diagnosis}</p>}
                    <div className="mt-2 space-y-1">
                      {p.items?.map((item, idx) => (
                        <div key={idx} className="text-xs bg-gray-50 p-2 rounded border border-gray-100 flex justify-between">
                          <span className="font-medium text-gray-800">{item.medication} {item.dosage}</span>
                          <span className="text-gray-500">{item.frequency} for {item.duration}</span>
                        </div>
                      ))}
                    </div>
                  </Card>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Invoices Tab */}
        {activeTab === "invoices" && (
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <h2 className="text-lg font-semibold text-gray-900">Billing & Invoices</h2>
              <Link href="/billing">
                <Button size="sm" className="flex items-center gap-1.5 bg-primary text-white">
                  <Plus className="w-4 h-4" /> Create Invoice
                </Button>
              </Link>
            </div>

            {tabLoading ? (
              <LoadingSpinner />
            ) : invoices.length === 0 ? (
              <Card className="p-8 text-center text-gray-500">No invoices generated for this patient.</Card>
            ) : (
              <div className="space-y-3">
                {invoices.map((inv) => (
                  <Link key={inv.id} href={`/billing/${inv.id}`}>
                    <Card className="p-4 mb-3 flex items-center justify-between border-gray-200 hover:border-primary/50 transition-colors cursor-pointer">
                      <div>
                        <div className="font-bold text-gray-900">{inv.invoice_number}</div>
                        <div className="text-xs text-gray-500">Date: {formatDate(inv.invoice_date)} • Due: {formatDate(inv.due_date)}</div>
                      </div>
                      <div className="text-right">
                        <div className="font-bold text-gray-900">{formatCurrency(inv.total_amount)}</div>
                        <div className="text-xs text-gray-500">Balance: {formatCurrency(inv.balance)}</div>
                      </div>
                      <Badge className={getStatusColor(inv.status)}>{inv.status}</Badge>
                    </Card>
                  </Link>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Timeline Tab */}
        {activeTab === "timeline" && (
          <div className="space-y-4">
            <h2 className="text-lg font-semibold text-gray-900">Patient Journey Timeline</h2>
            {tabLoading ? (
              <LoadingSpinner />
            ) : timeline.length === 0 ? (
              <Card className="p-8 text-center text-gray-500">No timeline history recorded yet.</Card>
            ) : (
              <div className="relative pl-6 space-y-6 before:absolute before:left-2.5 before:top-2 before:bottom-2 before:w-0.5 before:bg-gray-200">
                {timeline.map((event) => (
                  <div key={event.id} className="relative">
                    <div className="absolute -left-6 mt-1 w-3 h-3 rounded-full bg-primary ring-4 ring-white" />
                    <Card className="p-4 border-gray-200">
                      <div className="flex justify-between items-start mb-1">
                        <h4 className="font-semibold text-sm text-gray-900">{event.title}</h4>
                        <span className="text-xs text-gray-400">{formatDate(event.created_at)}</span>
                      </div>
                      {event.description && <p className="text-xs text-gray-600">{event.description}</p>}
                      {event.created_by_name && <p className="text-[11px] text-gray-400 mt-1">Recorded by {event.created_by_name}</p>}
                    </Card>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Add Note Modal */}
      <Modal isOpen={showNoteModal} onClose={() => setShowNoteModal(false)} title="Add Patient Note">
        <form onSubmit={handleAddNote} className="space-y-4">
          <Textarea
            label="Note Details"
            value={noteContent}
            onChange={(e) => setNoteContent(e.target.value)}
            rows={4}
            placeholder="Write clinical observations, treatment remarks, or administrative notes..."
            required
          />
          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              id="isClinical"
              checked={isClinicalNote}
              onChange={(e) => setIsClinicalNote(e.target.checked)}
              className="rounded border-gray-300 text-primary focus:ring-primary h-4 w-4"
            />
            <label htmlFor="isClinical" className="text-sm text-gray-700">
              Mark as Clinical Note (confidential dental/medical note)
            </label>
          </div>
          <div className="flex justify-end gap-3 pt-4 border-t">
            <Button type="button" variant="outline" onClick={() => setShowNoteModal(false)}>
              Cancel
            </Button>
            <Button type="submit" className="bg-primary text-white">
              Save Note
            </Button>
          </div>
        </form>
      </Modal>
    </PageWrapper>
  );
}
