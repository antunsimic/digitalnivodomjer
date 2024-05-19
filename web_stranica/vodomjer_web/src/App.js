import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Sidemenu from './components/Sidemenu';
import LoginPage from './components/LoginPage';
import LogoutPage from './components/LogoutPage';
import DatabasePage from './components/DatabasePage';
import './App.css';
import { AuthProvider } from './contexts/AuthContext';
import AuthStatusChecker from './components/AuthStatusChecker'; // Import the new component

import { DatabaseProvider } from './contexts/DatabaseProvider';  // Import the new provider

const App = () => {
  return (
    <AuthProvider>
      <DatabaseProvider>  {/* Add DatabaseProvider */}
        <Router>
          <AuthStatusChecker />
          <div className="App">
            <Navbar />
            <div className="content">
              <Sidemenu />
              <div className="main-content">
                <Routes>
                  <Route path="/login" element={<LoginPage />} />
                  <Route path="/logout" element={<LogoutPage />} />
                  <Route path="/baza" element={<DatabasePage />} />
                </Routes>
              </div>
            </div>
          </div>
        </Router>
      </DatabaseProvider>
    </AuthProvider>
  );
};

export default App;
