import React from "react";
import { Card } from "./Card";

interface StatsCardProps {
  title: string;
  value: string | number;
  icon: React.ReactNode;
  trend?: string;
}

export const StatsCard: React.FC<StatsCardProps> = ({ title, value, icon, trend }) => {
  return (
    <Card className="p-6">
      <div className="flex items-center">
        <div className="flex-shrink-0 bg-blue-50 rounded-md p-3">
          {React.cloneElement(icon as React.ReactElement, { className: "h-6 w-6 text-primary" })}
        </div>
        <div className="ml-5 w-0 flex-1">
          <dl>
            <dt className="text-sm font-medium text-gray-500 truncate">{title}</dt>
            <dd>
              <div className="text-2xl font-semibold text-gray-900">{value}</div>
            </dd>
          </dl>
        </div>
      </div>
      {trend && (
        <div className="mt-4 text-sm text-gray-500">
          <span className="text-green-600 font-medium">{trend}</span> since last month
        </div>
      )}
    </Card>
  );
};
