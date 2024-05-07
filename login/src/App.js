import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import LoginPage from './components/LoginPage';
import './App.css'; // Uvoz CSS datoteke

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<LoginPage />} />
        </Routes>
      </div>
    </Router>
  );
}

function Home() {
  return (
    <div className="right-corner">
      <Link to="/login">Log in</Link>
    </div>
  );
}

export default App;
