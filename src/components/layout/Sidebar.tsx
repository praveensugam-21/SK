"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { LayoutDashboard, Users, Calendar, Receipt, LogOut } from "lucide-react";
import { useAuth } from "@/lib/auth";
import { cn } from "@/lib/utils";

interface SidebarProps {
  onClose?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ onClose }) => {
  const pathname = usePathname();
  const { user, logout } = useAuth();

  const navItems = [
    { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
    { name: "Patients", href: "/patients", icon: Users },
    { name: "Appointments", href: "/appointments", icon: Calendar },
    { name: "Billing", href: "/billing", icon: Receipt },
  ];

  return (
    <div className="flex h-full flex-col bg-[#1e1e2d] text-white w-64 shadow-lg">
      <div className="flex h-16 shrink-0 items-center px-6 bg-[#1a1a2e]">
        <span className="text-xl font-bold tracking-wider text-white">Meridian Dental</span>
      </div>
      <div className="flex flex-1 flex-col overflow-y-auto pt-5 pb-4">
        <nav className="mt-5 flex-1 space-y-1 px-2">
          {navItems.map((item) => {
            const isActive = pathname.startsWith(item.href);
            return (
              <Link
                key={item.name}
                href={item.href}
                onClick={onClose}
                className={cn(
                  isActive ? "bg-primary text-white" : "text-gray-300 hover:bg-gray-800 hover:text-white",
                  "group flex items-center rounded-md px-2 py-2 text-sm font-medium transition-colors"
                )}
              >
                <item.icon className={cn("mr-3 h-5 w-5 shrink-0", isActive ? "text-white" : "text-gray-400 group-hover:text-gray-300")} />
                {item.name}
              </Link>
            );
          })}
        </nav>
      </div>
      <div className="flex shrink-0 bg-gray-900 p-4">
        <div className="w-full flex items-center justify-between">
          <div className="flex flex-col">
            <p className="text-sm font-medium text-white">{user?.full_name || 'User'}</p>
            <p className="text-xs text-gray-400 capitalize">{user?.role || 'Role'}</p>
          </div>
          <button onClick={logout} className="text-gray-400 hover:text-white p-2 rounded-md transition-colors" title="Sign out">
            <LogOut className="h-5 w-5" />
          </button>
        </div>
      </div>
    </div>
  );
};
