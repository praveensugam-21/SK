import React, { useState, useEffect } from "react";
import { Search, X } from "lucide-react";
import { Input } from "./Input";

interface SearchInputProps {
  value: string;
  onChange: (val: string) => void;
  placeholder?: string;
  className?: string;
}

export const SearchInput: React.FC<SearchInputProps> = ({ value, onChange, placeholder = "Search...", className }) => {
  const [localValue, setLocalValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => onChange(localValue), 300);
    return () => clearTimeout(timer);
  }, [localValue, onChange]);

  useEffect(() => {
    setLocalValue(value);
  }, [value]);

  return (
    <div className="relative">
      <Input
        value={localValue}
        onChange={(e) => setLocalValue(e.target.value)}
        placeholder={placeholder}
        icon={<Search className="h-4 w-4" />}
        className={className}
      />
      {localValue && (
        <button 
          className="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600"
          onClick={() => { setLocalValue(""); onChange(""); }}
        >
          <X className="h-4 w-4" />
        </button>
      )}
    </div>
  );
};
