"use client";

import React, { useState, useEffect } from "react";
import { useDentalChart } from "@/hooks/useDentalChart";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";

interface DentalChartProps {
  patientId: string;
}

export default function DentalChart({ patientId }: DentalChartProps) {
  const { records, loading, fetchChart, updateTooth } = useDentalChart(patientId);
  const [selectedTooth, setSelectedTooth] = useState<number | null>(null);

  useEffect(() => {
    fetchChart();
  }, [fetchChart]);

  const conditions = [
    { id: "healthy", label: "Healthy", color: "bg-white", tint: "bg-white border-gray-300 text-gray-700 hover:bg-gray-50" },
    { id: "cavity", label: "Cavity", color: "bg-red-500", tint: "bg-red-100 border-red-500 text-red-900 font-semibold" },
    { id: "filled", label: "Filled", color: "bg-blue-500", tint: "bg-blue-100 border-blue-500 text-blue-900 font-semibold" },
    { id: "crown", label: "Crown", color: "bg-yellow-500", tint: "bg-yellow-100 border-yellow-500 text-yellow-900 font-semibold" },
    { id: "root_canal", label: "Root Canal", color: "bg-orange-500", tint: "bg-orange-100 border-orange-500 text-orange-900 font-semibold" },
    { id: "missing", label: "Missing", color: "bg-gray-800", tint: "bg-gray-200 border-gray-700 text-gray-500 line-through" },
  ];

  const safeRecords = Array.isArray(records) ? records : [];

  const getToothStyle = (num: number) => {
    const record = safeRecords.find((r) => r.tooth_number === num);
    if (!record || record.condition === "healthy") {
      return "bg-white border-gray-300 text-gray-700 hover:bg-gray-50";
    }

    const cond = conditions.find((c) => c.id === record.condition);
    return cond ? cond.tint : "bg-white border-gray-300";
  };

  const handleConditionSelect = async (conditionId: string) => {
    if (selectedTooth === null) return;
    await updateTooth(selectedTooth, { condition: conditionId });
  };

  return (
    <Card className="p-6">
      <div className="mb-6">
        <h2 className="text-xl font-bold text-gray-900">Dental chart</h2>
        <p className="text-sm text-gray-500">Universal numbering, 1-32.</p>
      </div>

      <div className="flex flex-col items-center space-y-6 mb-8 overflow-x-auto pb-4">
        {/* Upper Jaw (1-16) */}
        <div>
          <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider block mb-2 text-center">Upper Jaw (1 - 16)</span>
          <div className="flex gap-2">
            {Array.from({ length: 16 }, (_, i) => i + 1).map((num) => (
              <button
                key={num}
                type="button"
                onClick={() => setSelectedTooth(num)}
                className={`w-9 h-9 sm:w-10 sm:h-10 rounded-md border-2 flex items-center justify-center text-sm font-medium transition-all shadow-sm ${getToothStyle(
                  num
                )} ${selectedTooth === num ? "ring-2 ring-primary ring-offset-2 scale-105" : ""}`}
              >
                {num}
              </button>
            ))}
          </div>
        </div>

        {/* Lower Jaw (17-32) */}
        <div>
          <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider block mb-2 text-center">Lower Jaw (17 - 32)</span>
          <div className="flex gap-2">
            {Array.from({ length: 16 }, (_, i) => i + 17).map((num) => (
              <button
                key={num}
                type="button"
                onClick={() => setSelectedTooth(num)}
                className={`w-9 h-9 sm:w-10 sm:h-10 rounded-md border-2 flex items-center justify-center text-sm font-medium transition-all shadow-sm ${getToothStyle(
                  num
                )} ${selectedTooth === num ? "ring-2 ring-primary ring-offset-2 scale-105" : ""}`}
              >
                {num}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="bg-gray-50 rounded-xl p-4 border border-gray-200">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <span className="text-sm font-medium text-gray-800">
            {selectedTooth ? (
              <span>
                Tooth <strong className="text-primary text-base">#{selectedTooth}</strong> selected — choose a condition:
              </span>
            ) : (
              "Click on any tooth number above to update its condition."
            )}
          </span>

          <div className="flex flex-wrap gap-2">
            {conditions.map((cond) => (
              <Button
                key={cond.id}
                variant="outline"
                size="sm"
                disabled={!selectedTooth}
                onClick={() => handleConditionSelect(cond.id)}
                className="flex items-center gap-1.5 text-xs font-medium bg-white"
              >
                <span className={`w-3 h-3 rounded-full ${cond.color} border border-gray-300`} />
                {cond.label}
              </Button>
            ))}
          </div>
        </div>
      </div>
    </Card>
  );
}
