import React, { useState, useEffect } from 'react';
import Papa from 'papaparse'; // Importing PapaParse for CSV parsing
import CandidateCard from '../components/CandidateCard';
import { Users, AlertTriangle, Star, Network, Activity } from 'lucide-react'; 
import { Card, CardContent, CardHeader, CardTitle } from '../components/card';
import dataCSV from '../Candidates.csv'; // Importing the CSV file directly

// Function to render the summary cards at the top
const renderOverview = () => (
  <div className="grid gap-2 md:grid-cols-5 lg:grid-cols-5 mb-6 text-sm">
    <Card className="p-2">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-1">
        <CardTitle className="text-xs font-medium">Total Candidates</CardTitle>
        <Users className="h-3 w-3 text-neutral-500 dark:text-neutral-400" />
      </CardHeader>
      <CardContent>
        <div className="text-xl font-bold">1000</div>
      </CardContent>
    </Card>
    <Card className="p-2">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-1">
        <CardTitle className="text-xs font-medium">Fraud Alerts</CardTitle>
        <AlertTriangle className="h-3 w-3 text-red-500" />
      </CardHeader>
      <CardContent>
        <div className="text-xl font-bold">31</div>
        <p className="text-xs text-neutral-500 dark:text-neutral-400"></p>
      </CardContent>
    </Card>
    <Card className="p-2">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-1">
        <CardTitle className="text-xs font-medium">Risk Score average</CardTitle>
        <Star className="h-3 w-3 text-yellow-400" />
      </CardHeader>
      <CardContent>
        <div className="text-xl font-bold">24.64</div>
        <p className="text-xs text-neutral-500 dark:text-neutral-400"></p>
      </CardContent>
    </Card>
    <Card className="p-2">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-1">
        <CardTitle className="text-xs font-medium">Hiring Score average</CardTitle>
        <Network className="h-3 w-3 text-neutral-500 dark:text-neutral-400" />
      </CardHeader>
      <CardContent>
        <div className="text-xl font-bold">33.59</div>
        <p className="text-xs text-neutral-500 dark:text-neutral-400"></p>
      </CardContent>
    </Card>
    <Card className="p-2">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-1">
        <CardTitle className="text-xs font-medium">Influence Score average</CardTitle>
        <Activity className="h-3 w-3 text-green-500" />
      </CardHeader>
      <CardContent>
        <div className="text-xl font-bold">77.2</div>
        <p className="text-xs text-neutral-500 dark:text-neutral-400"></p>
      </CardContent>
    </Card>
  </div>
);

// Main Overview Component
const Overview = () => {
  const [candidates, setCandidates] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filter, setFilter] = useState('all');
  const [sortOption, setSortOption] = useState('none'); // State for sorting option

  useEffect(() => {
    // Check if the file is correctly imported
    console.log('CSV File Imported:', dataCSV);

    // Parse the imported CSV data
    Papa.parse(dataCSV, {
      header: true,
      download: true, // Ensure the file is downloaded
      complete: (results) => {
        console.log('Parsed Results:', results); // Log parsed results
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
        console.error('Error parsing CSV:', error); // Log any errors
      },
    });
  }, []);

  console.log(candidates);

  // Handle search input
  const handleSearch = (e) => setSearchTerm(e.target.value);

  // Handle sorting option selection
  const handleSortOption = (e) => setSortOption(e.target.value);

  // Filter and sort candidates based on search and sorting options
  const filteredCandidates = candidates
    .filter((candidate) => {
      const candidateLastJob = candidate.lastJob ? candidate.lastJob.toLowerCase() : '';
      return candidateLastJob.includes(searchTerm.toLowerCase());
    })
    .sort((a, b) => {
      if (sortOption === 'risk_high_to_low') {
        return b.riskScore - a.riskScore; // Sort by risk score from high to low
      } else if (sortOption === 'risk_low_to_high') {
        return a.riskScore - b.riskScore; // Sort by risk score from low to high
      } else if (sortOption === 'hiring_high_to_low') {
        return b.hiringScore - a.hiringScore; // Sort by hiring score from high to low
      } else if (sortOption === 'hiring_low_to_high') {
        return a.hiringScore - b.hiringScore; // Sort by hiring score from low to high
      } else {
        return 0; // No sorting
      }
    });

  return (
    <div className="p-2">
      {/* Render Overview Summary Cards */}
      {renderOverview()}

      {/* Search and Filter */}
      <div className="flex mb-2">
        <input
          type="text"
          placeholder="Search by last job..."
          className="p-1 border rounded-lg w-full text-xs"
          value={searchTerm}
          onChange={handleSearch}
        />

        <select className="ml-2 p-1 border rounded-lg text-xs" value={filter} onChange={(e) => setFilter(e.target.value)}>
          <option value="all">All</option>
          <option value="high">High Risk Score</option>
          <option value="medium">Medium Risk Score</option>
          <option value="low">Low Risk Score</option>
        </select>

        {/* Sorting Options */}
        <select className="ml-2 p-1 border rounded-lg text-xs" value={sortOption} onChange={handleSortOption}>
          <option value="none">Sort By</option>
          <option value="risk_high_to_low">Risk Score: High to Low</option>
          <option value="risk_low_to_high">Risk Score: Low to High</option>
          <option value="hiring_high_to_low">Hiring Score: High to Low</option>
          <option value="hiring_low_to_high">Hiring Score: Low to High</option>
        </select>
      </div>

      {/* Scrollable Container for Candidate Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-2 overflow-y-auto" style={{ maxHeight: '80vh', paddingBottom: '10px' }}>
        {filteredCandidates.map((candidate, index) => (
          <CandidateCard key={index} candidate={candidate} />
        ))}
      </div>
    </div>
  );
};

export default Overview;
