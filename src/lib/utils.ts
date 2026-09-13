import { type ClassValue, clsx } from "clsx";
import { format, parseISO } from "date-fns";

export function cn(...inputs: ClassValue[]) {
  return clsx(inputs);
}

export function formatDate(date: string) {
  if (!date) return "";
  return format(parseISO(date), "MMM d, yyyy");
}

export function formatTime(time: string) {
  if (!time) return "";
  const [hours, minutes] = time.split(':');
  const d = new Date();
  d.setHours(parseInt(hours, 10));
  d.setMinutes(parseInt(minutes, 10));
  return format(d, "h:mm a");
}

export function formatCurrency(amount: number) {
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
  }).format(amount);
}

export function getStatusColor(status: string) {
  switch (status.toLowerCase()) {
    case 'completed': case 'paid': case 'confirmed':
      return 'bg-green-100 text-green-800';
    case 'pending':
      return 'bg-yellow-100 text-yellow-800';
    case 'cancelled':
      return 'bg-red-100 text-red-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
}

export function getInitials(name: string) {
  if (!name) return "";
  return name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
}

export function calculateAge(dob: string) {
  if (!dob) return 0;
  const birthDate = new Date(dob);
  const today = new Date();
  let age = today.getFullYear() - birthDate.getFullYear();
  const m = today.getMonth() - birthDate.getMonth();
  if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
    age--;
  }
  return age;
}
