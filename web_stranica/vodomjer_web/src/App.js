import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Navbar from './components/Navbar';
import Sidemenu from './components/Sidemenu';
import LoginPage from './components/LoginPage';
import LogoutPage from './components/LogoutPage';
import DatabasePage from './components/DatabasePage';
import './App.css';

function App() {
  const [loggedIn, setLoggedIn] = useState(false);

  return (
    <Router>
      <div className="App">
      <Navbar loggedIn={loggedIn} setLoggedIn={setLoggedIn} />
     
        <div className="content">
        <Sidemenu />
          <Routes>
            <Route path="/login" element={<LoginPage loggedIn={loggedIn} setLoggedIn={setLoggedIn}/>} />
            <Route path="/logout" element={<LogoutPage loggedIn={loggedIn} setLoggedIn={setLoggedIn}/>} />
            <Route path="/baza" element={<DatabasePage />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
