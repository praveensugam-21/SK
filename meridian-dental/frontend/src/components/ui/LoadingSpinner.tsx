import React from "react";
import { Loader2 } from "lucide-react";

export const LoadingSpinner: React.FC<{ message?: string }> = ({ message }) => (
  <div className="flex flex-col items-center justify-center p-4">
    <Loader2 className="h-8 w-8 animate-spin text-primary" />
    {message && <p className="mt-2 text-sm text-gray-500">{message}</p>}
  </div>
);
