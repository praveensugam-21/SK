import React from "react";
import { cn } from "@/lib/utils";
import { LoadingSpinner } from "./LoadingSpinner";
import { EmptyState } from "./EmptyState";

interface Column<T> {
  header: string;
  accessor: keyof T | ((row: T) => React.ReactNode);
  className?: string;
}

interface TableProps<T> {
  columns: Column<T>[];
  data: T[];
  isLoading?: boolean;
  emptyMessage?: string;
  onRowClick?: (row: T) => void;
  className?: string;
}

export function Table<T>({ columns, data, isLoading, emptyMessage = "No data found", onRowClick, className }: TableProps<T>) {
  if (isLoading) {
    return <div className="p-8 flex justify-center"><LoadingSpinner /></div>;
  }

  if (!data || data.length === 0) {
    return <EmptyState title={emptyMessage} />;
  }

  return (
    <div className={cn("w-full overflow-auto rounded-md border border-gray-200 bg-white", className)}>
      <table className="w-full text-sm text-left">
        <thead className="bg-gray-50 border-b border-gray-200 text-gray-700">
          <tr>
            {columns.map((col, i) => (
              <th key={i} className={cn("px-4 py-3 font-medium", col.className)}>
                {col.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {data.map((row, i) => (
            <tr 
              key={i} 
              onClick={() => onRowClick?.(row)}
              className={cn("bg-white hover:bg-gray-50 transition-colors", onRowClick && "cursor-pointer")}
            >
              {columns.map((col, j) => (
                <td key={j} className={cn("px-4 py-3", col.className)}>
                  {typeof col.accessor === 'function' ? col.accessor(row) : (row[col.accessor] as React.ReactNode)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
