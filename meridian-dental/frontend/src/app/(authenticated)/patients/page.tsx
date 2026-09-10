"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { PageWrapper } from "@/components/layout/PageWrapper";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { SearchInput } from "@/components/ui/SearchInput";
import { Table } from "@/components/ui/Table";
import { Pagination } from "@/components/ui/Pagination";
import { Modal } from "@/components/ui/Modal";
import { Textarea } from "@/components/ui/Textarea";
import { usePatients } from "@/hooks/usePatients";
import { calculateAge } from "@/lib/utils";
import { Patient } from "@/types";

export default function PatientsPage() {
  const router = useRouter();
  const { patients, total, loading, fetchPatients, createPatient } = usePatients();
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const pageSize = 10;
  
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState<Partial<Patient>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    fetchPatients(search, page, pageSize);
  }, [fetchPatients, search, page]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      await createPatient(formData);
      setIsModalOpen(false);
      setFormData({});
      fetchPatients(search, 1, pageSize);
    } catch (err) {
      // Error handled by hook
    } finally {
      setIsSubmitting(false);
    }
  };

  const columns = [
    { header: "Full name", accessor: (row: Patient) => <div className="font-medium text-gray-900">{row.full_name}</div> },
    { header: "Date of birth", accessor: (row: Patient) => row.date_of_birth ? `${row.date_of_birth} (${calculateAge(row.date_of_birth)}y)` : "-" },
    { header: "Phone", accessor: "phone" },
    { header: "Email", accessor: (row: Patient) => row.email || "-" },
    { header: "Notes", accessor: (row: Patient) => <div className="truncate max-w-xs">{row.notes || "-"}</div> },
  ];

  return (
    <PageWrapper 
      title="Patients" 
      action={<Button onClick={() => setIsModalOpen(true)}>+ Add patient</Button>}
    >
      <div className="mb-6 max-w-md">
        <SearchInput value={search} onChange={(val) => { setSearch(val); setPage(1); }} placeholder="Search patients..." />
      </div>

      <Table 
        columns={columns} 
        data={patients} 
        isLoading={loading} 
        onRowClick={(row) => router.push(`/patients/${row.id}`)} 
      />
      
      {!loading && total > 0 && (
        <Pagination 
          page={page} 
          totalPages={Math.ceil(total / pageSize)} 
          onPageChange={setPage} 
        />
      )}

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Add Patient">
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input 
            label="Full name" 
            required 
            value={formData.full_name || ""} 
            onChange={(e) => setFormData({...formData, full_name: e.target.value})} 
          />
          <div className="grid grid-cols-2 gap-4">
            <Input 
              type="date" 
              label="Date of birth" 
              value={formData.date_of_birth || ""} 
              onChange={(e) => setFormData({...formData, date_of_birth: e.target.value})} 
            />
            <Input 
              label="Phone" 
              required 
              value={formData.phone || ""} 
              onChange={(e) => setFormData({...formData, phone: e.target.value})} 
            />
          </div>
          <Input 
            type="email" 
            label="Email" 
            value={formData.email || ""} 
            onChange={(e) => setFormData({...formData, email: e.target.value})} 
          />
          <Textarea 
            label="Notes" 
            placeholder="Allergies, preferences, medical history..." 
            value={formData.notes || ""} 
            onChange={(e) => setFormData({...formData, notes: e.target.value})} 
          />
          <div className="flex justify-end gap-3 pt-4">
            <Button variant="outline" type="button" onClick={() => setIsModalOpen(false)}>Cancel</Button>
            <Button type="submit" isLoading={isSubmitting}>Save patient</Button>
          </div>
        </form>
      </Modal>
    </PageWrapper>
  );
}
