// src/components/ProgressBar.js
import React from 'react';

const ProgressBar = ({ score }) => {
  const progress = score + '%';
  return (
    <div className="w-full bg-gray-200 rounded-full h-4">
      <div className="bg-blue-600 h-4 rounded-full" style={{ width: progress }}></div>
    </div>
  );
};

export default ProgressBar;
