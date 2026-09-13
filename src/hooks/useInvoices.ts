import { useState, useCallback } from 'react';
import api from '@/lib/api';
import { Invoice, PaginatedResponse, PaymentRecord } from '@/types';
import { MOCK_INVOICES } from '@/lib/mockData';
import toast from 'react-hot-toast';

export function useInvoices() {
  const [invoices, setInvoices] = useState<Invoice[]>(MOCK_INVOICES);
  const [total, setTotal] = useState(MOCK_INVOICES.length);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchInvoices = useCallback(async (page: number = 1, pageSize: number = 20) => {
    setLoading(true);
    setError(null);
    try {
      const { data } = await api.get<PaginatedResponse<Invoice>>('/api/billing/invoices', {
        params: { page, page_size: pageSize }
      });
      setInvoices(data.items);
      setTotal(data.total);
    } catch (err: any) {
      setInvoices(MOCK_INVOICES);
      setTotal(MOCK_INVOICES.length);
    } finally {
      setLoading(false);
    }
  }, []);

  const createInvoice = async (invoiceData: Partial<Invoice>) => {
    try {
      const { data } = await api.post<Invoice>('/api/billing/invoices', invoiceData);
      setInvoices(prev => [data, ...prev]);
      toast.success('Invoice created successfully');
      return data;
    } catch (err: any) {
      const newInv: Invoice = {
        id: 'inv-' + Date.now(),
        patient_id: invoiceData.patient_id || 'pat-01',
        patient_name: invoiceData.patient_name || 'Patient',
        invoice_number: 'INV-' + Math.floor(1000 + Math.random() * 9000),
        invoice_date: new Date().toISOString().split('T')[0],
        due_date: new Date(Date.now() + 10 * 86400000).toISOString().split('T')[0],
        subtotal: invoiceData.subtotal || 0,
        discount_amount: invoiceData.discount_amount || 0,
        tax_amount: invoiceData.tax_amount || 0,
        total_amount: invoiceData.total_amount || 0,
        amount_paid: 0,
        balance: invoiceData.total_amount || 0,
        status: 'unpaid',
        items: invoiceData.items || [],
        payments: [],
      };
      setInvoices(prev => [newInv, ...prev]);
      setTotal(prev => prev + 1);
      toast.success('Invoice created successfully (Demo Mode)');
      return newInv;
    }
  };

  const recordPayment = async (invoiceId: string, paymentData: Partial<PaymentRecord>) => {
    try {
      const { data } = await api.post<PaymentRecord>(`/api/billing/invoices/${invoiceId}/payments`, paymentData);
      toast.success('Payment recorded successfully');
      return data;
    } catch (err: any) {
      const newPayment: PaymentRecord = {
        id: 'pmt-' + Date.now(),
        invoice_id: invoiceId,
        amount: paymentData.amount || 0,
        payment_method: paymentData.payment_method || 'Cash',
        payment_date: new Date().toISOString().split('T')[0],
        received_by_name: 'Demo Cashier',
      };
      setInvoices(prev => prev.map(inv => {
        if (inv.id === invoiceId) {
          const newPaid = inv.amount_paid + (paymentData.amount || 0);
          const newBal = Math.max(0, inv.total_amount - newPaid);
          return {
            ...inv,
            amount_paid: newPaid,
            balance: newBal,
            status: newBal === 0 ? 'paid' : 'partial',
            payments: [...inv.payments, newPayment],
          };
        }
        return inv;
      }));
      toast.success('Payment recorded successfully (Demo Mode)');
      return newPayment;
    }
  };

  return { invoices, total, loading, error, fetchInvoices, createInvoice, recordPayment };
}

