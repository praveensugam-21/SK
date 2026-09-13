import React from "react";

interface PageWrapperProps {
  children: React.ReactNode;
  title?: string;
  action?: React.ReactNode;
}

export const PageWrapper: React.FC<PageWrapperProps> = ({ children, title, action }) => {
  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 md:px-8 py-8">
      {(title || action) && (
        <div className="flex items-center justify-between mb-8">
          {title && <h1 className="text-2xl font-semibold text-gray-900">{title}</h1>}
          {action && <div>{action}</div>}
        </div>
      )}
      <div>{children}</div>
    </div>
  );
};
