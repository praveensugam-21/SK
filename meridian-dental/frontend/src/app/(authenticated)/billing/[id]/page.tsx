"use client";

import React, { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { PageWrapper } from "@/components/layout/PageWrapper";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";
import { Select } from "@/components/ui/Select";
import api from "@/lib/api";
import { useInvoices } from "@/hooks/useInvoices";
import { Invoice } from "@/types";
import { formatCurrency, formatDate, getStatusColor } from "@/lib/utils";

export default function InvoiceDetailPage() {
  const { id } = useParams() as { id: string };
  const [invoice, setInvoice] = useState<Invoice | null>(null);
  const [loading, setLoading] = useState(true);
  const { recordPayment } = useInvoices();

  const [isPaymentModalOpen, setIsPaymentModalOpen] = useState(false);
  const [paymentAmount, setPaymentAmount] = useState<number>(0);
  const [paymentMethod, setPaymentMethod] = useState("Cash");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const fetchInvoice = async () => {
    try {
      const { data } = await api.get<Invoice>(`/api/billing/invoices/${id}`);
      setInvoice(data);
      setPaymentAmount(data.balance);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchInvoice();
  }, [id]);

  const handleRecordPayment = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      await recordPayment(id, {
        amount: paymentAmount,
        payment_method: paymentMethod,
        payment_date: new Date().toISOString()
      });
      setIsPaymentModalOpen(false);
      fetchInvoice();
    } catch (err) {
      // Error handled by hook
    } finally {
      setIsSubmitting(false);
    }
  };

  if (loading) return <PageWrapper><LoadingSpinner /></PageWrapper>;
  if (!invoice) return <PageWrapper>Invoice not found</PageWrapper>;

  return (
    <PageWrapper>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Invoice {invoice.invoice_number}</h1>
          <div className="flex gap-4 text-sm text-gray-500">
            <span>Date: {formatDate(invoice.invoice_date)}</span>
            <span>Due: {formatDate(invoice.due_date)}</span>
            <Badge className={getStatusColor(invoice.status)}>{invoice.status}</Badge>
          </div>
        </div>
        <div className="flex gap-3">
          <Button variant="outline">Download PDF</Button>
          {invoice.balance > 0 && (
            <Button onClick={() => setIsPaymentModalOpen(true)}>Record Payment</Button>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="md:col-span-2 space-y-6">
          <Card className="p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Patient Information</h3>
            <p className="font-medium">{invoice.patient_name}</p>
          </Card>

          <Card className="overflow-hidden">
            <div className="p-6 border-b border-gray-200">
              <h3 className="text-lg font-medium text-gray-900">Line Items</h3>
            </div>
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Description</th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Qty</th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Price</th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {invoice.items?.map((item, i) => (
                  <tr key={i}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{item.description}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 text-right">{item.quantity}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 text-right">{formatCurrency(item.unit_price)}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right font-medium">{formatCurrency(item.amount)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </Card>
        </div>

        <div className="space-y-6">
          <Card className="p-6 bg-gray-50">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Summary</h3>
            <div className="space-y-3 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-500">Subtotal</span>
                <span className="font-medium">{formatCurrency(invoice.subtotal)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Tax</span>
                <span className="font-medium">{formatCurrency(invoice.tax_amount)}</span>
              </div>
              <div className="pt-3 border-t border-gray-200 flex justify-between text-base font-bold">
                <span>Total</span>
                <span>{formatCurrency(invoice.total_amount)}</span>
              </div>
              <div className="flex justify-between text-green-600">
                <span>Paid</span>
                <span>-{formatCurrency(invoice.amount_paid)}</span>
              </div>
              <div className="pt-3 border-t border-gray-200 flex justify-between text-lg font-bold text-gray-900">
                <span>Balance Due</span>
                <span>{formatCurrency(invoice.balance)}</span>
              </div>
            </div>
          </Card>
        </div>
      </div>

      <Modal isOpen={isPaymentModalOpen} onClose={() => setIsPaymentModalOpen(false)} title="Record Payment">
        <form onSubmit={handleRecordPayment} className="space-y-4">
          <Input 
            type="number" 
            label="Amount (₹)" 
            required 
            max={invoice.balance}
            value={paymentAmount} 
            onChange={(e) => setPaymentAmount(parseFloat(e.target.value))} 
          />
          <Select 
            label="Payment Method" 
            required
            value={paymentMethod} 
            onChange={(e) => setPaymentMethod(e.target.value)}
            options={[
              { label: "Cash", value: "Cash" },
              { label: "UPI", value: "UPI" },
              { label: "Card", value: "Card" },
              { label: "Bank Transfer", value: "Bank Transfer" },
            ]}
          />
          <div className="flex justify-end gap-3 pt-4">
            <Button variant="outline" type="button" onClick={() => setIsPaymentModalOpen(false)}>Cancel</Button>
            <Button type="submit" isLoading={isSubmitting}>Record Payment</Button>
          </div>
        </form>
      </Modal>
    </PageWrapper>
  );
}
