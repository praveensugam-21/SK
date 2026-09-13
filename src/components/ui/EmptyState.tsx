import React from "react";
import { Inbox } from "lucide-react";
import { Button } from "./Button";

interface EmptyStateProps {
  title: string;
  description?: string;
  actionLabel?: string;
  onAction?: () => void;
}

export const EmptyState: React.FC<EmptyStateProps> = ({ title, description, actionLabel, onAction }) => (
  <div className="flex flex-col items-center justify-center p-8 text-center bg-gray-50 rounded-lg border border-dashed border-gray-300">
    <div className="h-12 w-12 rounded-full bg-gray-100 flex items-center justify-center mb-4">
      <Inbox className="h-6 w-6 text-gray-400" />
    </div>
    <h3 className="text-sm font-medium text-gray-900">{title}</h3>
    {description && <p className="mt-1 text-sm text-gray-500">{description}</p>}
    {actionLabel && onAction && (
      <div className="mt-4">
        <Button variant="outline" size="sm" onClick={onAction}>{actionLabel}</Button>
      </div>
    )}
  </div>
);
