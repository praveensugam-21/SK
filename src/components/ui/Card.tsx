import React from "react";
import { cn } from "@/lib/utils";

export const Card: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ className, children, ...props }) => {
  return (
    <div className={cn("bg-white rounded-lg shadow-sm border border-gray-200", className)} {...props}>
      {children}
    </div>
  );
};
