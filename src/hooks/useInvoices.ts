import { useState, useCallback } from 'react';
import api from '@/lib/api';
import { Invoice, PaginatedResponse, PaymentRecord } from '@/types';
import toast from 'react-hot-toast';

export function useInvoices() {
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [total, setTotal] = useState(0);
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
      setError(err.message || 'Failed to fetch invoices');
      toast.error('Failed to fetch invoices');
    } finally {
      setLoading(false);
    }
  }, []);

  const createInvoice = async (invoiceData: Partial<Invoice>) => {
    try {
      const { data } = await api.post<Invoice>('/api/billing/invoices', invoiceData);
      toast.success('Invoice created successfully');
      return data;
    } catch (err: any) {
      toast.error(err.response?.data?.detail || 'Failed to create invoice');
      throw err;
    }
  };

  const recordPayment = async (invoiceId: string, paymentData: Partial<PaymentRecord>) => {
    try {
      const { data } = await api.post<PaymentRecord>(`/api/billing/invoices/${invoiceId}/payments`, paymentData);
      toast.success('Payment recorded successfully');
      return data;
    } catch (err: any) {
      toast.error(err.response?.data?.detail || 'Failed to record payment');
      throw err;
    }
  };

  return { invoices, total, loading, error, fetchInvoices, createInvoice, recordPayment };
}
