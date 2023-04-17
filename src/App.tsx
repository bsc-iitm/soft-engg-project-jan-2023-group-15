import React, { useState } from 'react';
import Option1 from './pages/Student/Student';
import Option2 from './pages/Admin/Admin';
import Option3 from './pages/SupportStaff/SupportStaff';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import FAQ from './pages/Student/FAQ'
import Profile from './pages/Student/Profile';
import './App.css';
import AdminFAQ from './pages/Admin/AdminFAQ';
import AdminProfile from './pages/Admin/AdminProfile';
import Staff from './pages/Admin/Staff';
import SupportStaffFAQ from './pages/SupportStaff/SupportStaffFAQ';
import SupportStaffProfile from './pages/SupportStaff/SupportStaffProfile';


function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
            <Route path="/" element={<HomePage/>} />
            <Route path="/option1" element={<Option1 />} />
            <Route path="/option1/FAQ" element={<FAQ />} />
            <Route path="/option1/Profile" element={<Profile />} />
            <Route path="/option2" element={<Option2 />} />
            <Route path="/option2/FAQ" element={<AdminFAQ />} />
            <Route path="/option2/Profile" element={<AdminProfile />} />
            <Route path="/option2/Staff" element={<Staff />} />
            <Route path="/option3" element={<Option3 />} />
            <Route path="/option3/FAQ" element={<SupportStaffFAQ />} />
            <Route path="/option3/Profile" element={<SupportStaffProfile />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
