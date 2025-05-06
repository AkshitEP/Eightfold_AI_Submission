import React, { useState, useEffect } from 'react';
import Select from 'react-select'; // Import react-select for searchable dropdown
import Papa from 'papaparse';
import dataCSV from '../Candidates.csv'; // Importing the CSV file directly

const CandidateComparison = () => {
  const [candidates, setCandidates] = useState([]);
  const [candidate1, setCandidate1] = useState(null);
  const [candidate2, setCandidate2] = useState(null);

  useEffect(() => {
    // Parse the CSV file
    Papa.parse(dataCSV, {
      header: true,
      download: true,
      complete: (results) => {
        const formattedCandidates = results.data.map((item, index) => ({
          id: index, // Assign a unique ID
          name: index,
          position: item['Last Job'], // Adjust this if needed
          fraudScore: item['Risk Score'],
          relevanceScore: item['Hiring Score'],
          experience: item['Work Experience'],
          department: item['Influence'], // Adjust this based on your CSV structure
          skills: [
            { name: item['Skill 1'] },
            { name: item['Skill 2'] },
            { name: item['Skill 3'] }
          ],
        }));
        setCandidates(formattedCandidates);
      },
      error: (error) => {
        console.error("Error parsing CSV: ", error);
      }
    });
  }, []);

  // Handle selection of candidates
  const handleCandidate1Change = (selectedOption) => {
    setCandidate1(selectedOption);
  };

  const handleCandidate2Change = (selectedOption) => {
    setCandidate2(selectedOption);
  };

  // Convert candidate data to format usable by react-select
  const candidateOptions = candidates.map((candidate) => ({
    value: candidate.id,
    label: `Candidate ${candidate.name} - ${candidate.position}`,
    candidate,
  }));

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <h2 className="text-3xl font-bold mb-6 text-center text-gray-800">Candidate Comparison</h2>

      {/* Candidate Selection */}
      <div className="flex justify-center space-x-8 mb-6">
        <div className="w-1/3">
          <label className="block mb-2 text-sm font-medium text-gray-600">Select Candidate 1</label>
          <Select
            options={candidateOptions}
            onChange={handleCandidate1Change}
            value={candidate1}
            placeholder="Search for Candidate 1"
            className="rounded-lg"
            theme={(theme) => ({
              ...theme,
              colors: {
                ...theme.colors,
                primary25: 'lightgray', // Highlight on hover
                primary: 'black', // Selected option
              },
            })}
          />
        </div>
        <div className="w-1/3">
          <label className="block mb-2 text-sm font-medium text-gray-600">Select Candidate 2</label>
          <Select
            options={candidateOptions}
            onChange={handleCandidate2Change}
            value={candidate2}
            placeholder="Search for Candidate 2"
            className="rounded-lg"
            theme={(theme) => ({
              ...theme,
              colors: {
                ...theme.colors,
                primary25: 'lightgray', // Highlight on hover
                primary: 'black', // Selected option
              },
            })}
          />
        </div>
      </div>

      {/* Comparison Table */}
      {candidate1 && candidate2 && (
        <div className="bg-white shadow-lg rounded-lg p-6 transition-all duration-300 ease-in-out hover:shadow-xl">
          <table className="w-full text-left table-fixed border-collapse">
            <thead>
              <tr>
                <th className="w-1/4 px-4 py-2 font-semibold border-b-2 border-gray-300"></th>
                <th className="w-1/4 px-4 py-2 font-semibold border-b-2 border-gray-300 text-black">{candidate1.label}</th>
                <th className="w-1/4 px-4 py-2 font-semibold border-b-2 border-gray-300 text-black">{candidate2.label}</th>
              </tr>
            </thead>
            <tbody>
              {/* Position */}
              <tr className="hover:bg-gray-100 transition-colors duration-200">
                <td className="border px-4 py-2 font-medium text-gray-600">Position</td>
                <td className="border px-4 py-2">{candidate1.candidate.position}</td>
                <td className="border px-4 py-2">{candidate2.candidate.position}</td>
              </tr>
              {/* Experience */}
              <tr className="hover:bg-gray-100 transition-colors duration-200">
                <td className="border px-4 py-2 font-medium text-gray-600">Experience</td>
                <td className="border px-4 py-2">{candidate1.candidate.experience} years</td>
                <td className="border px-4 py-2">{candidate2.candidate.experience} years</td>
              </tr>
              {/* Risk Score */}
              <tr className="hover:bg-gray-100 transition-colors duration-200">
                <td className="border px-4 py-2 font-medium text-gray-600">Risk Score</td>
                <td className="border px-4 py-2">{candidate1.candidate.fraudScore}%</td>
                <td className="border px-4 py-2">{candidate2.candidate.fraudScore}%</td>
              </tr>
              {/* Relevance Score */}
              <tr className="hover:bg-gray-100 transition-colors duration-200">
                <td className="border px-4 py-2 font-medium text-gray-600">Relevance Score</td>
                <td className="border px-4 py-2">{candidate1.candidate.relevanceScore}%</td>
                <td className="border px-4 py-2">{candidate2.candidate.relevanceScore}%</td>
              </tr>
              {/* Skills */}
              <tr className="hover:bg-gray-100 transition-colors duration-200">
                <td className="border px-4 py-2 font-medium text-gray-600">Skills</td>
                <td className="border px-4 py-2">
                  {candidate1.candidate.skills.map(skill => skill.name).join(', ')}
                </td>
                <td className="border px-4 py-2">
                  {candidate2.candidate.skills.map(skill => skill.name).join(', ')}
                </td>
              </tr>
              {/* Department */}
              <tr className="hover:bg-gray-100 transition-colors duration-200">
                <td className="border px-4 py-2 font-medium text-gray-600">Department</td>
                <td className="border px-4 py-2">{candidate1.candidate.department}</td>
                <td className="border px-4 py-2">{candidate2.candidate.department}</td>
              </tr>
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default CandidateComparison;
