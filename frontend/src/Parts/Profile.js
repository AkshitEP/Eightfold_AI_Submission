import React, { useEffect, useState, useMemo } from 'react';
import { useParams } from 'react-router-dom';
import { csv } from 'd3-fetch';
import Gauge from '../components/Gauge'; // Import the reusable Gauge component
import { ChevronDown, ChevronUp } from 'lucide-react'; // For dropdown arrows
import dataCSV from '../Candidates.csv'; // Importing the CSV file directly
import Papa from 'papaparse';

// Helper function to determine color for risk (high = red, low = green)
const getRiskGaugeColor = (score) => {
  if (score <= 33) return 'text-green-500'; // Low score (green)
  if (score <= 66) return 'text-orange-500'; // Medium score (orange)
  return 'text-red-500'; // High score (red)
};

// Helper function to determine color for hiring score (low = red, high = green)
const getHiringScoreColor = (score) => {
  if (score <= 33) return 'text-red-500'; // Low score (red)
  if (score <= 66) return 'text-orange-500'; // Medium score (orange)
  return 'text-green-500'; // High score (green)
};

// Helper function to determine color for influential score (mid-range color logic)
const getInfluentialScoreColor = (score) => {
  if (score <= 33) return 'text-yellow-500'; // Low score (yellow)
  if (score <= 66) return 'text-orange-500'; // Medium score (orange)
  return 'text-blue-500'; // High score (blue)
};

const Profile = () => {
  const { id } = useParams(); // Get the profile ID from the URL
  const [profileData, setProfileData] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [candidate, setCandidate] = useState(null); // State to hold the candidate profile
  const [jobHistory, setJobHistory] = useState([]);
  const [education, setEducation] = useState([]);
  const [skills, setSkills] = useState([]);

  // State to manage collapsed sections
  const [showJobHistory, setShowJobHistory] = useState(false);
  const [showEducation, setShowEducation] = useState(false);
  const [showSkills, setShowSkills] = useState(false);

  useEffect(() => {
    // Parse the imported CSV data and find the candidate by ID
    Papa.parse(dataCSV, {
      header: true,
      download: true,
      complete: (results) => {
        if (results && results.data) {
          const parsedCandidates = results.data.map((candidate) => ({
            id: candidate.ID,
            lastJob: candidate['Last Job'],
            influence: parseInt(candidate.Influence, 10),
            riskScore: parseFloat(candidate['Risk Score']),
            hiringScore: parseFloat(candidate['Hiring Score']),
            workExperience: parseInt(candidate['Work Experience'], 10),
            skills: [
              { name: candidate['Skill 1'] },
              { name: candidate['Skill 2'] },
              { name: candidate['Skill 3'] },
            ],
          }));

          // Find the candidate by ID
          const foundCandidate = parsedCandidates.find((c) => c.id === id);
          setCandidate(foundCandidate); // Set the found candidate to state
        } else {
          console.error('No data found in CSV results');
        }
      },
      error: (error) => {
        console.error('Error parsing CSV:', error); // Log any errors
      },
    });
  }, [id]);

  useEffect(() => {
    // Load the profile data from JSON
    const loadProfile = async () => {
      try {
        const response = await import(`../resumes/${id}.json`);
        setProfileData(response);

        // Set job history, education, and skills from JSON data
        if (response && response.details) {
          setJobHistory(response.details.job_history || []);
          setEducation(response.details.education || []);
          setSkills(response.skills?.skills || []);
        }

      } catch (error) {
        console.error('Error loading profile data:', error);
      }
    };

    loadProfile();
  }, [id]);

  useEffect(() => {
    // Load recommendations from the merged recommendations file
    const loadRecommendations = async () => {
      try {
        const response = await import(`../Merged LORs/Merged_Recommendations_for_Resume_${id}.json`);
        setRecommendations(response.recommendations || []);
      } catch (error) {
        console.error('Error loading recommendations:', error);
      }
    };

    loadRecommendations();
  }, [id]);

  // Function to normalize skill names for matching
  const normalizeSkillName = (name) => name.trim().toLowerCase();

  // Collect verified skills from recommendations whenever recommendations change
  const verifiedSkillsSet = useMemo(() => {
    const set = new Set();

    recommendations.forEach((rec) => {
      const verifiedSkills = rec.recommendation.output.verified_skills;
      if (verifiedSkills && Array.isArray(verifiedSkills)) {
        verifiedSkills.forEach((skill) => {
          set.add(normalizeSkillName(skill));
        });
      }
    });

    return set;
  }, [recommendations]);

  // Separate skills into verified and unverified whenever skills or verifiedSkillsSet change
  const { verifiedSkills, unverifiedSkills } = useMemo(() => {
    const verified = [];
    const unverified = [];

    if (skills && skills.length > 0) {
      skills.forEach((skill) => {
        if (verifiedSkillsSet.has(normalizeSkillName(skill.name))) {
          verified.push(skill);
        } else {
          unverified.push(skill);
        }
      });
    }

    return { verifiedSkills: verified, unverifiedSkills: unverified };
  }, [skills, verifiedSkillsSet]);

  if (!candidate || !profileData) {
    return (
      <div className="text-center p-6">
        <p className="text-xl font-medium text-gray-700">Loading profile...</p>
      </div>
    );
  }

  // Pull in risk score, hiring score, and influential score
  const formattedRiskScore = candidate.riskScore?.toFixed(2);
  const formattedHiringScore = (candidate.hiringScore * 10).toFixed(2);
  const influentialScore = candidate.influence * 10 || 60;

  return (
    <div className="p-6 max-w-5xl mx-auto bg-white rounded-lg shadow-lg">
      <h2 className="text-3xl font-bold text-gray-900 mb-6 text-center">Candidate Profile</h2>

      {/* Gauges for Risk Score, Hiring Score, and Influential */}
      <div className="flex justify-around items-center mb-8">
        <Gauge
          score={formattedRiskScore}
          label="Risk Score"
          colorClass={getRiskGaugeColor(candidate.riskScore)}
          strokeClass={getRiskGaugeColor(candidate.riskScore)}
        />

        <Gauge
          score={formattedHiringScore}
          label="Hiring Score"
          colorClass={getHiringScoreColor(candidate.hiringScore)}
          strokeClass={getHiringScoreColor(candidate.hiringScore)}
        />

        <Gauge
          score={influentialScore}
          label="Influential"
          colorClass={getInfluentialScoreColor(influentialScore)}
          strokeClass={getInfluentialScoreColor(influentialScore)}
        />
      </div>

      {/* Job History with Dropdown */}
      {jobHistory && (
        <div className="mb-8">
          <div
            className="flex justify-between items-center mb-4 cursor-pointer"
            onClick={() => setShowJobHistory(!showJobHistory)}
          >
            <h3 className="text-2xl font-semibold text-gray-800 flex items-center">Job History</h3>
            {showJobHistory ? <ChevronUp className="h-6 w-6" /> : <ChevronDown className="h-6 w-6" />}
          </div>
          {showJobHistory && (
            <ul className="grid grid-cols-1 gap-6">
              {jobHistory.map((job, index) => (
                <li key={index} className="p-4 bg-gray-100 rounded-lg shadow-md">
                  <h4 className="text-xl font-semibold text-gray-800">{job.role_name}</h4>
                  <p className="text-sm text-gray-600">
                    {job.start_date} - {job.end_date}
                  </p>
                  <p className="text-base text-gray-700 mt-2">{job.work_description}</p>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}

      {/* Education with Dropdown */}
      {education && (
        <div className="mb-8">
          <div
            className="flex justify-between items-center mb-4 cursor-pointer"
            onClick={() => setShowEducation(!showEducation)}
          >
            <h3 className="text-2xl font-semibold text-gray-800 flex items-center">Education</h3>
            {showEducation ? <ChevronUp className="h-6 w-6" /> : <ChevronDown className="h-6 w-6" />}
          </div>
          {showEducation && (
            <ul className="grid grid-cols-1 gap-6">
              {education.map((edu, index) => (
                <li key={index} className="p-4 bg-gray-100 rounded-lg shadow-md">
                  <h4 className="text-xl font-semibold text-gray-800">{edu.university}</h4>
                  <p className="text-sm text-gray-600">
                    {edu.start_date} - {edu.end_date || 'Present'}
                  </p>
                  <p className="text-base text-gray-700 mt-2">
                    {edu.level} in {edu.domain}
                  </p>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}

      {/* Skills with Dropdown */}
      {skills.length > 0 && (
        <div className="mb-8">
          <div
            className="flex justify-between items-center mb-4 cursor-pointer"
            onClick={() => setShowSkills(!showSkills)}
          >
            <h3 className="text-2xl font-semibold text-gray-800 flex items-center">Skills</h3>
            {showSkills ? <ChevronUp className="h-6 w-6" /> : <ChevronDown className="h-6 w-6" />}
          </div>
          {showSkills && (
            <>
              {verifiedSkills.length > 0 && (
                <div className="mb-4">
                  <h4 className="text-xl font-semibold text-green-700">Verified Skills</h4>
                  <ul className="grid grid-cols-1 gap-6">
                    {verifiedSkills.map((skill, index) => (
                      <li key={index} className="p-4 bg-green-100 rounded-lg shadow-md">
                        <h5 className="text-lg font-semibold text-gray-800">{skill.name}</h5>
                        <p className="text-sm text-gray-600">Level: {skill.level}</p>
                        <p className="text-base text-gray-700 mt-2">{skill.explanation}</p>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              {unverifiedSkills.length > 0 && (
                <div>
                  <h4 className="text-xl font-semibold text-red-700">Unverified Skills</h4>
                  <ul className="grid grid-cols-1 gap-6">
                    {unverifiedSkills.map((skill, index) => (
                      <li key={index} className="p-4 bg-red-100 rounded-lg shadow-md">
                        <h5 className="text-lg font-semibold text-gray-800">{skill.name}</h5>
                        <p className="text-sm text-gray-600">Level: {skill.level}</p>
                        <p className="text-base text-gray-700 mt-2">{skill.explanation}</p>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </>
          )}
        </div>
      )}
    </div>
  );
};

export default Profile;
