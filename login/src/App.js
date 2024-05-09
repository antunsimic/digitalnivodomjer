import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import LoginPage from './components/LoginPage';
import LogoutPage from './components/LogoutPage'
import './App.css'; // Uvoz CSS datoteke

function App() {

  const[loggedIn, setLoggedIn] = useState(false);

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Home loggedIn={loggedIn}/>} />
          <Route path="/login" element={<LoginPage loggedIn={loggedIn} setLoggedIn={setLoggedIn}/>} />
          <Route path="/logout" element={<LogoutPage loggedIn={loggedIn} setLoggedIn={setLoggedIn}/>} />
        </Routes>
      </div>
    </Router>
  );
}

function Home( {loggedIn} ) {

  console.log('Logged in home: ', loggedIn)
  return (
    <div className="right-corner">
      {loggedIn ? (
        <Link to="/logout">Log out</Link>
      ) : (
        <Link to="/login">Log in</Link>
      )}
    </div>
  );
}

export default App;
