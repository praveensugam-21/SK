"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import { Input } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";
import toast from "react-hot-toast";

export default function LoginPage() {
  const router = useRouter();
  const { login } = useAuth();
  const [email, setEmail] = useState("admin@meridian.dental");
  const [password, setPassword] = useState("Admin@123");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password) {
      toast.error("Please enter email and password");
      return;
    }
    setLoading(true);
    try {
      await login(email, password);
      toast.success("Signed in successfully!");
      router.push("/dashboard");
    } catch (err: any) {
      const detail = err.response?.data?.detail || "Invalid email or password";
      toast.error(detail);
    } finally {
      setLoading(false);
    }
  };

  const handleQuickFill = (demoEmail: string, demoPass: string) => {
    setEmail(demoEmail);
    setPassword(demoPass);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8 bg-white p-8 sm:p-10 rounded-2xl shadow-xl border border-gray-100">
        <div className="text-center">
          <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-[#1e1e2d] text-white shadow-md mb-4 font-bold text-2xl">
            MD
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-gray-900 tracking-tight">
            Meridian Dental
          </h2>
          <p className="mt-1 text-sm text-gray-500">
            Dental Clinic Management System
          </p>
        </div>

        <form className="mt-8 space-y-5" onSubmit={handleSubmit}>
          <div className="space-y-4">
            <Input
              id="email"
              type="email"
              label="Email address"
              required
              placeholder="name@meridian.dental"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <Input
              id="password"
              type="password"
              label="Password"
              required
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <div>
            <Button type="submit" fullWidth isLoading={loading} className="py-2.5 bg-primary hover:bg-primary/90 text-white font-semibold shadow-md transition-all">
              Sign In
            </Button>
          </div>
        </form>

        {/* Quick Demo Logins for fast testing */}
        <div className="pt-4 border-t border-gray-100">
          <p className="text-xs font-semibold uppercase tracking-wider text-gray-400 text-center mb-3">
            Quick Fill Demo Credentials
          </p>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs">
            <button
              type="button"
              onClick={() => handleQuickFill("admin@meridian.dental", "Admin@123")}
              className="px-2 py-1.5 bg-gray-50 hover:bg-gray-100 border border-gray-200 rounded-lg text-gray-700 font-medium transition-colors text-center"
            >
              👑 Admin
            </button>
            <button
              type="button"
              onClick={() => handleQuickFill("dentist@meridian.dental", "Dentist@123")}
              className="px-2 py-1.5 bg-gray-50 hover:bg-gray-100 border border-gray-200 rounded-lg text-gray-700 font-medium transition-colors text-center"
            >
              🦷 Dentist
            </button>
            <button
              type="button"
              onClick={() => handleQuickFill("receptionist@meridian.dental", "Reception@123")}
              className="px-2 py-1.5 bg-gray-50 hover:bg-gray-100 border border-gray-200 rounded-lg text-gray-700 font-medium transition-colors text-center"
            >
              📋 Reception
            </button>
            <button
              type="button"
              onClick={() => handleQuickFill("accountant@meridian.dental", "Account@123")}
              className="px-2 py-1.5 bg-gray-50 hover:bg-gray-100 border border-gray-200 rounded-lg text-gray-700 font-medium transition-colors text-center"
            >
              💰 Accountant
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
