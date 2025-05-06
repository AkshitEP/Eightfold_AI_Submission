import React, { useEffect, useState } from 'react';
import Papa from 'papaparse'; // Importing PapaParse for CSV parsing
import { Card, CardContent, CardHeader, CardTitle } from "../components/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "../components/table";
import dataCSV from '../Candidates.csv'; // Importing the CSV file directly

const FraudAlerts = () => {
  const [fraudCandidates, setFraudCandidates] = useState([]);

  useEffect(() => {
    // Parse the imported CSV data
    Papa.parse(dataCSV, {
      header: true,
      download: true, // Ensure the file is downloaded
      complete: (results) => {
        if (results && results.data) {
          const parsedCandidates = results.data.map((candidate) => ({
            id: candidate.ID,
            position: candidate['Position'], // Assuming you have a column for Position
            riskScore: parseFloat(candidate['Risk Score']),
          }));
          
          // Filter candidates with risk score >= 70 and sort them in descending order
          const filteredFraudCandidates = parsedCandidates
            .filter(candidate => candidate.riskScore >= 70)
            .sort((a, b) => b.riskScore - a.riskScore);
          
          setFraudCandidates(filteredFraudCandidates);
        } else {
          console.error('No data found in CSV results');
        }
      },
      error: (error) => {
        console.error('Error parsing CSV:', error); // Log any errors
      },
    });
  }, []);

  const renderFraudAlerts = () => (
    <Card>
      <CardHeader>
        <CardTitle>Fraud Alerts</CardTitle>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>ID</TableHead>
              <TableHead>Position</TableHead> {/* New header for Position */}
              <TableHead>Fraud Risk Score</TableHead>
              <TableHead>Recommended Action</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {fraudCandidates.map((candidate) => (
              <TableRow key={candidate.id}>
                <TableCell>{candidate.id}</TableCell> {/* Show ID */}
                <TableCell>{candidate.position}</TableCell> {/* Show Position */}
                <TableCell className="text-red-500">{candidate.riskScore}</TableCell> {/* Show risk score */}
                <TableCell>Immediate Review</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );

  return (
    <div>
      {renderFraudAlerts()}
    </div>
  );
};

export default FraudAlerts;
