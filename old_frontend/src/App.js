import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './Dashboard';
import Sidebar from './Sidebar';

function App() {
  return (
    <Router>
      <div className="flex min-h-screen bg-gray-900 text-gray-100">
        <Sidebar />
        <main className="flex-1 p-6">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/analytics" element={<div className="text-white">Analytics Page</div>} />
            <Route path="/records" element={<div className="text-white">Records Page</div>} />
            <Route path="/settings" element={<div className="text-white">Settings Page</div>} />
            <Route path="/help" element={<div className="text-white">Help Page</div>} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;