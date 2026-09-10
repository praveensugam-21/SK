export interface User { id: string; email: string; full_name: string; role: 'admin' | 'dentist' | 'receptionist' | 'accountant'; clinic_id: string; phone?: string; specialization?: string; is_active: boolean; }

export interface Patient { id: string; patient_id_display: string; full_name: string; date_of_birth?: string; gender?: string; phone: string; email?: string; address?: string; emergency_contact_name?: string; emergency_contact_phone?: string; blood_group?: string; allergies?: string; medical_history?: string; current_medications?: string; insurance_provider?: string; insurance_id?: string; notes?: string; status: string; created_at: string; updated_at: string; }

export interface Appointment { id: string; patient_id: string; dentist_id: string; patient_name: string; dentist_name: string; date: string; start_time: string; end_time: string; duration_minutes: number; appointment_type: string; status: string; notes?: string; created_at: string; }

export interface ToothRecord { tooth_number: number; condition: string; surfaces?: { mesial?: boolean; distal?: boolean; occlusal?: boolean; buccal?: boolean; lingual?: boolean; }; diagnosis?: string; treatment?: string; notes?: string; updated_at?: string; }

export interface TreatmentPlan { id: string; patient_id: string; dentist_id: string; dentist_name: string; title: string; description?: string; status: string; total_estimated_cost: number; treatments: Treatment[]; created_at: string; }

export interface Treatment { id: string; plan_id?: string; patient_id: string; tooth_number?: number; diagnosis?: string; treatment_type: string; description?: string; cost: number; status: string; notes?: string; completed_at?: string; }

export interface Invoice { id: string; patient_id: string; patient_name: string; invoice_number: string; invoice_date: string; due_date: string; subtotal: number; discount_amount: number; tax_amount: number; total_amount: number; amount_paid: number; balance: number; status: string; items: InvoiceItem[]; payments: PaymentRecord[]; }

export interface InvoiceItem { id: string; description: string; treatment_id?: string; quantity: number; unit_price: number; discount: number; amount: number; }

export interface PaymentRecord { id: string; invoice_id: string; amount: number; payment_method: string; transaction_reference?: string; payment_date: string; received_by_name?: string; }

export interface Prescription { id: string; patient_id: string; dentist_id: string; dentist_name: string; date: string; diagnosis?: string; notes?: string; items: PrescriptionItem[]; }

export interface PrescriptionItem { medication: string; dosage: string; frequency: string; duration: string; instructions?: string; }

export interface Note { id: string; patient_id: string; author_name: string; content: string; note_type: string; is_clinical: boolean; created_at: string; }

export interface TimelineEvent { id: string; event_type: string; title: string; description?: string; created_by_name?: string; created_at: string; }

export interface DashboardStats { total_patients: number; todays_appointments: number; completed_appointments: number; pending_appointments: number; cancelled_appointments: number; todays_revenue: number; outstanding_amount: number; new_patients_this_month: number; }

export interface TodaySchedule { appointment_id: string; patient_name: string; time: string; type: string; duration: number; status: string; }

export interface PaginatedResponse<T> { items: T[]; total: number; page: number; page_size: number; total_pages: number; }
