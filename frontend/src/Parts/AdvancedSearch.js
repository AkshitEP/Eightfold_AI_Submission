import React, { useState, useEffect } from 'react';
import Papa from 'papaparse'; // Importing PapaParse for CSV parsing
import CandidateCard from '../components/CandidateCard';
import dataCSV from '../Candidates.csv'; // Importing the CSV file directly

const AdvancedSearch = () => {
  const [candidates, setCandidates] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(false);
  const [matchedCandidateIds, setMatchedCandidateIds] = useState([]);

  useEffect(() => {
    // Parse the CSV data
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
          setCandidates(parsedCandidates);
        } else {
          console.error('No data found in CSV results');
        }
      },
      error: (error) => {
        console.error('Error parsing CSV:', error);
      },
    });
  }, []);

  const fetchSearchResults = async (query) => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:5000/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
      });
      if (!response.ok) throw new Error('Network response was not ok');
      const results = await response.json();
      const ids = Array.from(new Set(results.map((result) => result.user_id)));
      setMatchedCandidateIds(ids);
    } catch (error) {
      console.error('Error fetching search results:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    if (searchTerm) {
      await fetchSearchResults(searchTerm);
    }
  };

  const filteredCandidates = candidates.filter((candidate) =>
    matchedCandidateIds.includes(parseInt(candidate.id, 10))
  );

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      {/* Search bar */}
      <div className="w-full max-w-xl p-6 bg-white shadow-md rounded-lg mt-10">
        <div className="flex items-center space-x-4">
          <input
            type="text"
            placeholder="Search for candidates..."
            className="flex-grow p-3 text-lg border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          <button
            onClick={handleSearch}
            className="px-6 py-3 bg-blue-500 text-white rounded-full hover:bg-blue-600 transition duration-200"
          >
            Search
          </button>
        </div>
      </div>

      {loading && (
        <div className="mt-6">
          <div className="loader"></div>
          <p className="text-gray-500">Searching...</p>
        </div>
      )}

      {/* Display results */}
      {filteredCandidates.length > 0 && !loading && (
        <div className="w-full max-w-3xl mt-8 bg-white shadow-md rounded-lg p-6">
          <h2 className="text-2xl font-semibold text-gray-800 mb-6">
            Search Results
          </h2>
          <ul>
            {filteredCandidates.map((candidate) => (
              <li key={candidate.id} className="mb-6">
                <CandidateCard candidate={candidate} />
              </li>
            ))}
          </ul>
        </div>
      )}

      {!loading && filteredCandidates.length === 0 && searchTerm && (
        <div className="text-center text-gray-500 mt-6">
          No results found for "<strong>{searchTerm}</strong>"
        </div>
      )}
    </div>
  );
};

export default AdvancedSearch;
