import React, { useState } from 'react';
import { Input } from "./components/input";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./components/tabs";

import Overview from './Parts/Overview'; // Import Overview component
import CandidateComparison from './Parts/CandidateComparsion'; // Import CandidateComparison component
import InfluentialOverview from './Parts/InfluentialOverview'; // Import InfluentialOverview component
import AdvancedSearch from './Parts/AdvancedSearch'; // Import AdvancedSearch component

export function App() {
  const [activeTab, setActiveTab] = useState('overview'); // Default active tab

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      {/* Top Navigation */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-gray-900">Satya</h1>
            <div className="flex items-center">
              <Input type="search" placeholder="Search..." className="mr-2" />
            </div>
          </div>
        </div>
      </header>

      {/* Tabs Section */}
      <div className="flex-1 overflow-hidden">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full h-full flex flex-col">
          <TabsList className="flex justify-center space-x-12 p-4 bg-gray-50">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="candidate-comparison">Candidate Comparison</TabsTrigger>
            <TabsTrigger value="influential-overview">Influential Overview</TabsTrigger>
            <TabsTrigger value="advanced-search">Advanced Search</TabsTrigger> {/* New Tab */}
          </TabsList>

          {/* Tabs Content */}
          <div className="flex-1 overflow-y-auto">
            <TabsContent value="overview" className="h-full">
              <Overview />
            </TabsContent>
            <TabsContent value="candidate-comparison" className="h-full">
              <CandidateComparison />
            </TabsContent>
            <TabsContent value="influential-overview" className="h-full">
              <InfluentialOverview />
            </TabsContent>
            <TabsContent value="advanced-search" className="h-full"> {/* Add content for AdvancedSearch */}
              <AdvancedSearch />
            </TabsContent>
          </div>
        </Tabs>
      </div>
    </div>
  );
}

export default App;
