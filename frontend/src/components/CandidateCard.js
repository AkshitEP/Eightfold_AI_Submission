import React from 'react';
import { Link } from 'react-router-dom';
import Gauge from '../components/Gauge'; // Import the reusable Gauge component

// Helper function to determine color for risk (high = red, low = green)
const getRiskGaugeColor = (score) => {
  if (score <= 33) return 'text-green-500'; // Low score (green)
  if (score <= 66) return 'text-orange-500'; // Medium score (orange)
  return 'text-red-500'; // High score (red)
};

// Helper function to determine color for hiring score (inverted logic: low = red, high = green)
const getHiringScoreColor = (score) => {
  if (score <= 33) return 'text-red-500'; // Low score (red)
  if (score <= 66) return 'text-orange-500'; // Medium score (orange)
  return 'text-green-500'; // High score (green)
};

// The CandidateCard component
const CandidateCard = ({ candidate }) => {
  const {
    id,
    lastJob,
    workExperience,
    riskScore,
    hiringScore,
    skills,
  } = candidate;

  const formattedHiringScore = (hiringScore).toFixed(2);
  const formattedRiskScore = riskScore.toFixed(2);

  return (
    <div className="p-2 bg-white shadow-md rounded-lg mb-4">
      <h2 className="text-lg font-bold mb-2">
        <Link to={`/profile/${candidate.id}`} className="text-blue-500 hover:underline mb-4">
          Candidate {candidate.id}
        </Link>
      </h2>
      <p className="text-xs text-gray-600 mb-1">- <b>{lastJob}</b></p>
      <p className="text-xs text-gray-600 mb-2">- <b>{workExperience} years of experience</b> </p>

      <div className="flex justify-between items-center mb-4">
        {/* Risk Score Gauge */}
        <Gauge
          score={formattedRiskScore}
          label="Risk Score"
          colorClass={getRiskGaugeColor(riskScore)}
          strokeClass={getRiskGaugeColor(riskScore)}
        />

        {/* Hiring Score Gauge */}
        <Gauge
          score={formattedHiringScore}
          label="Hiring Score"
          colorClass={getHiringScoreColor(formattedHiringScore)}
          strokeClass={getHiringScoreColor(formattedHiringScore)}
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

export default CandidateCard;
