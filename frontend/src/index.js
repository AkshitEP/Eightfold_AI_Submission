// index.js
import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './index.css';
import App from './App';
import Profile from './Parts/Profile'; // Make sure to import the Profile component
import InfluentialOverview from './Parts/InfluentialOverview'; // Import the new page


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<App />} /> {/* Home page */}
        <Route path="/profile/:id" element={<Profile />} /> {/* Profile page */}
        <Route path="/influential-overview" element={<InfluentialOverview />} /> 
      </Routes>
    </Router>
  </React.StrictMode>
);
