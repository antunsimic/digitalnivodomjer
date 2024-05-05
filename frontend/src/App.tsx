import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import DatabasePage from './components/DatabasePage';
import './App.css';


function App() {

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/database_page" element={<DatabasePage />} />
        </Routes>
      </div>
    </Router>
  );
}

function Home() {
  return (
    <div>
      <Link to="/database_page">Database Page</Link>
    </div>
  );
}

export default App;