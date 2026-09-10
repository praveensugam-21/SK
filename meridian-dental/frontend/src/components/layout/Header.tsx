import React from "react";
import { Menu } from "lucide-react";
import { useAuth } from "@/lib/auth";

interface HeaderProps {
  onMenuClick: () => void;
  title?: string;
}

export const Header: React.FC<HeaderProps> = ({ onMenuClick, title }) => {
  const { user } = useAuth();
  
  return (
    <div className="sticky top-0 z-10 flex h-16 flex-shrink-0 bg-white shadow-sm border-b border-gray-200 lg:hidden">
      <button
        type="button"
        className="border-r border-gray-200 px-4 text-gray-500 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary lg:hidden"
        onClick={onMenuClick}
      >
        <span className="sr-only">Open sidebar</span>
        <Menu className="h-6 w-6" aria-hidden="true" />
      </button>
      <div className="flex flex-1 justify-between px-4 sm:px-6 lg:px-8">
        <div className="flex flex-1 items-center">
          {title && <h1 className="text-lg font-semibold text-gray-900">{title}</h1>}
        </div>
        <div className="ml-4 flex items-center md:ml-6">
          <div className="flex items-center gap-2">
            <span className="text-sm font-medium text-gray-700">{user?.full_name}</span>
          </div>
        </div>
      </div>
    </div>
  );
};
