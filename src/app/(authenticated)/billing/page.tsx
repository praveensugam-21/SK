"use client";

import React, { useEffect, useState, useMemo } from "react";
import { useRouter } from "next/navigation";
import { PageWrapper } from "@/components/layout/PageWrapper";
import { Button } from "@/components/ui/Button";
import { Table } from "@/components/ui/Table";
import { Badge } from "@/components/ui/Badge";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";
import { Select } from "@/components/ui/Select";
import { Pagination } from "@/components/ui/Pagination";
import { useInvoices } from "@/hooks/useInvoices";
import { usePatients } from "@/hooks/usePatients";
import { formatCurrency, formatDate, getStatusColor } from "@/lib/utils";
import { Invoice } from "@/types";
import { Plus, Trash2 } from "lucide-react";
import toast from "react-hot-toast";

interface LineItemInput {
  description: string;
  quantity: number;
  unit_price: number;
  discount: number;
}

export default function BillingPage() {
  const router = useRouter();
  const { invoices, total, loading, fetchInvoices, createInvoice } = useInvoices();
  const { patients, fetchPatients } = usePatients();
  
  const [page, setPage] = useState(1);
  const pageSize = 10;

  // New Invoice Modal
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedPatientId, setSelectedPatientId] = useState("");
  const [dueDate, setDueDate] = useState(() => {
    const d = new Date();
    d.setDate(d.getDate() + 15);
    return d.toISOString().split("T")[0];
  });
  const [discountAmount, setDiscountAmount] = useState(0);
  const [taxAmount, setTaxAmount] = useState(0);
  const [notes, setNotes] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const [lineItems, setLineItems] = useState<LineItemInput[]>([
    { description: "General Dental Consultation", quantity: 1, unit_price: 500, discount: 0 },
  ]);

  useEffect(() => {
    fetchInvoices(page, pageSize);
    fetchPatients(1, 100);
  }, [fetchInvoices, fetchPatients, page]);

  const outstandingTotal = useMemo(() => {
    return invoices.reduce((acc, inv) => acc + (Number(inv.balance) || 0), 0);
  }, [invoices]);

  const calculatedSubtotal = useMemo(() => {
    return lineItems.reduce((acc, item) => {
      const itemTotal = (Number(item.quantity) || 1) * (Number(item.unit_price) || 0) - (Number(item.discount) || 0);
      return acc + Math.max(0, itemTotal);
    }, 0);
  }, [lineItems]);

  const calculatedTotal = useMemo(() => {
    return Math.max(0, calculatedSubtotal - (Number(discountAmount) || 0) + (Number(taxAmount) || 0));
  }, [calculatedSubtotal, discountAmount, taxAmount]);

  const handleAddLineItem = () => {
    setLineItems([...lineItems, { description: "", quantity: 1, unit_price: 0, discount: 0 }]);
  };

  const handleRemoveLineItem = (index: number) => {
    if (lineItems.length <= 1) return;
    setLineItems(lineItems.filter((_, i) => i !== index));
  };

  const handleLineItemChange = (index: number, field: keyof LineItemInput, value: any) => {
    const updated = [...lineItems];
    updated[index] = { ...updated[index], [field]: value };
    setLineItems(updated);
  };

  const handleCreateInvoice = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedPatientId) {
      toast.error("Please select a patient");
      return;
    }
    const validItems = lineItems.filter((item) => item.description.trim() && item.unit_price > 0);
    if (validItems.length === 0) {
      toast.error("Please add at least one line item with description and price");
      return;
    }

    setIsSubmitting(true);
    try {
      await createInvoice({
        patient_id: selectedPatientId,
        due_date: dueDate,
        discount_amount: Number(discountAmount) || 0,
        tax_amount: Number(taxAmount) || 0,
        notes,
        items: validItems.map((item) => ({
          description: item.description,
          quantity: Number(item.quantity) || 1,
          unit_price: Number(item.unit_price),
          discount: Number(item.discount) || 0,
          amount: (Number(item.quantity) || 1) * Number(item.unit_price) - (Number(item.discount) || 0),
        })),
      } as any);

      setIsModalOpen(false);
      // Reset
      setLineItems([{ description: "", quantity: 1, unit_price: 0, discount: 0 }]);
      fetchInvoices(page, pageSize);
    } catch (err) {
      // Handled in hook
    } finally {
      setIsSubmitting(false);
    }
  };

  const columns = [
    { header: "Invoice #", accessor: "invoice_number", className: "font-semibold text-primary" },
    { header: "Patient", accessor: "patient_name" },
    { header: "Date", accessor: (row: Invoice) => formatDate(row.invoice_date) },
    { header: "Due Date", accessor: (row: Invoice) => formatDate(row.due_date) },
    { header: "Total", accessor: (row: Invoice) => formatCurrency(row.total_amount) },
    { header: "Balance", accessor: (row: Invoice) => formatCurrency(row.balance) },
    {
      header: "Status",
      accessor: (row: Invoice) => <Badge className={getStatusColor(row.status)}>{row.status}</Badge>,
    },
  ];

  const patientOptions = patients.map((p) => ({
    label: `${p.full_name} (${p.patient_id_display}) - ${p.phone}`,
    value: p.id,
  }));

  return (
    <PageWrapper
      title="Billing"
      action={
        <Button onClick={() => setIsModalOpen(true)} className="bg-primary text-white">
          + New Invoice
        </Button>
      }
    >
      <div className="mb-6 p-4 bg-blue-50 text-blue-900 rounded-lg border border-blue-100 flex items-center justify-between">
        <div>
          <span className="font-bold text-xl">{formatCurrency(outstandingTotal)}</span>
          <span className="ml-2 text-blue-700">
            outstanding across {invoices.filter((i) => (Number(i.balance) || 0) > 0).length} invoice(s)
          </span>
        </div>
      </div>

      <Table
        columns={columns}
        data={invoices}
        isLoading={loading}
        onRowClick={(row) => router.push(`/billing/${row.id}`)}
      />

      {!loading && total > 0 && (
        <div className="mt-4">
          <Pagination
            page={page}
            totalPages={Math.ceil(total / pageSize)}
            onPageChange={setPage}
          />
        </div>
      )}

      {/* New Invoice Modal */}
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Create New Invoice" size="lg">
        <form onSubmit={handleCreateInvoice} className="space-y-4">
          <Select
            label="Select Patient"
            required
            placeholder="Choose patient..."
            value={selectedPatientId}
            onChange={(e) => setSelectedPatientId(e.target.value)}
            options={patientOptions}
          />

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              type="date"
              label="Due Date"
              required
              value={dueDate}
              onChange={(e) => setDueDate(e.target.value)}
            />
            <Input
              type="text"
              label="Invoice Note"
              placeholder="e.g. Treatment follow-up invoice"
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
            />
          </div>

          {/* Line items */}
          <div className="space-y-3 pt-2">
            <div className="flex justify-between items-center">
              <label className="block text-sm font-semibold text-gray-700">Treatment / Service Line Items</label>
              <Button type="button" size="sm" variant="outline" onClick={handleAddLineItem} className="flex items-center gap-1">
                <Plus className="w-3.5 h-3.5" /> Add Item
              </Button>
            </div>

            <div className="space-y-2">
              {lineItems.map((item, idx) => (
                <div key={idx} className="flex items-center gap-2 p-3 bg-gray-50 rounded-lg border border-gray-200">
                  <div className="flex-1">
                    <Input
                      placeholder="Item / Treatment (e.g. Root Canal, Crown, Scaling)"
                      required
                      value={item.description}
                      onChange={(e) => handleLineItemChange(idx, "description", e.target.value)}
                    />
                  </div>
                  <div className="w-20">
                    <Input
                      type="number"
                      placeholder="Qty"
                      min={1}
                      required
                      value={item.quantity}
                      onChange={(e) => handleLineItemChange(idx, "quantity", parseInt(e.target.value) || 1)}
                    />
                  </div>
                  <div className="w-28">
                    <Input
                      type="number"
                      placeholder="Price (₹)"
                      min={0}
                      required
                      value={item.unit_price}
                      onChange={(e) => handleLineItemChange(idx, "unit_price", parseFloat(e.target.value) || 0)}
                    />
                  </div>
                  {lineItems.length > 1 && (
                    <button
                      type="button"
                      onClick={() => handleRemoveLineItem(idx)}
                      className="p-2 text-red-500 hover:text-red-700 transition-colors"
                      title="Remove item"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Totals Calculation */}
          <div className="p-4 bg-gray-100 rounded-lg space-y-2 text-sm">
            <div className="flex justify-between text-gray-600">
              <span>Subtotal:</span>
              <span className="font-medium">{formatCurrency(calculatedSubtotal)}</span>
            </div>
            <div className="flex justify-between items-center text-gray-600">
              <span>Discount (₹):</span>
              <input
                type="number"
                min={0}
                className="w-28 text-right px-2 py-1 bg-white border border-gray-300 rounded text-sm"
                value={discountAmount}
                onChange={(e) => setDiscountAmount(parseFloat(e.target.value) || 0)}
              />
            </div>
            <div className="flex justify-between items-center text-gray-600">
              <span>Tax (₹):</span>
              <input
                type="number"
                min={0}
                className="w-28 text-right px-2 py-1 bg-white border border-gray-300 rounded text-sm"
                value={taxAmount}
                onChange={(e) => setTaxAmount(parseFloat(e.target.value) || 0)}
              />
            </div>
            <div className="pt-2 border-t border-gray-300 flex justify-between text-base font-bold text-gray-900">
              <span>Total Invoice Amount:</span>
              <span className="text-primary text-lg">{formatCurrency(calculatedTotal)}</span>
            </div>
          </div>

          <div className="flex justify-end gap-3 pt-4 border-t">
            <Button variant="outline" type="button" onClick={() => setIsModalOpen(false)}>
              Cancel
            </Button>
            <Button type="submit" isLoading={isSubmitting} className="bg-primary text-white">
              Create Invoice
            </Button>
          </div>
        </form>
      </Modal>
    </PageWrapper>
  );
}
