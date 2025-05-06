import React from 'react';
import { Link } from 'react-router-dom';
import Gauge from '../components/Gauge'; // Import the reusable Gauge component

// Helper function to determine color for influence score (low = red, high = green)
const getInfluenceGaugeColor = (score) => {
    if (score <= 70) return 'text-red-500'; // Low score (red)
    if (score <= 90) return 'text-orange-500'; // Medium score (orange)
    return 'text-green-500'; // High score (green)
  };

// The CandidateCard component for InfluentialOverview
const CandidateCardInfluential = ({ candidate }) => {
  const {
    id,
    lastJob,
    workExperience,
    influence, // Use influence instead of risk/hiring score
    skills,
  } = candidate;

  const formattedInfluence = influence.toFixed(2) * 10;

  return (
    <div className="p-2 bg-white shadow-md rounded-lg mb-4">
      <h2 className="text-lg font-bold mb-2">
        <Link to={`/profile/${candidate.id}`} className="text-blue-500 hover:underline mb-4">
          Candidate {candidate.id}
        </Link>
      </h2>
      <p className="text-xs text-gray-600 mb-1">- <b>{lastJob}</b></p>
      <p className="text-xs text-gray-600 mb-2">- <b>{workExperience} years of experience</b> </p>

      {/* Influence Gauge */}
      <div className="flex justify-center items-center mb-4">
        <Gauge
          score={formattedInfluence}
          label="Influence"
          colorClass={getInfluenceGaugeColor(influence)}
          strokeClass={getInfluenceGaugeColor(influence)}
        />
      </div>

      <div className="flex flex-wrap gap-1 mt-2">
        {skills.slice(0, 3).map((skill, index) => (
          <span key={index} className="bg-blue-200 text-blue-800 text-xs font-semibold px-2 py-1 rounded-full">
            {skill.name}
          </span>
        ))}
      </div>
    </div>
  );
};

export default CandidateCardInfluential;
