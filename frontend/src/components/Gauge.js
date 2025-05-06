// components/Gauge.js
import React from 'react';

// Helper function to generate stroke-dasharray based on score
const calculateStrokeDasharray = (score) => `${(score / 100) * 75} 100`;

// The Gauge component
const Gauge = ({ score, label, colorClass, strokeClass }) => {
  return (
    <div className="relative size-40">
      <svg className="rotate-[135deg] size-full" viewBox="0 0 36 36" xmlns="http://www.w3.org/2000/svg">
        {/* Background Circle */}
        <circle cx="18" cy="18" r="16" fill="none" className="stroke-current text-gray-200" strokeWidth="1" strokeDasharray="75 100"></circle>
        {/* Gauge Progress */}
        <circle cx="18" cy="18" r="16" fill="none" className={`stroke-current ${strokeClass}`} strokeWidth="2" strokeDasharray={calculateStrokeDasharray(score)}></circle>
      </svg>
      <div className="absolute top-1/2 start-1/2 transform -translate-x-1/2 -translate-y-1/2 text-center">
        <span className={`text-4xl font-bold ${colorClass}`}>{score}</span>
        <span className={`block text-xs ${colorClass}`}>{label}</span>
      </div>
    </div>
  );
};

export default Gauge;
