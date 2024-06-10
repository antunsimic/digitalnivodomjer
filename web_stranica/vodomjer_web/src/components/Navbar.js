import React from 'react';
import '../assets/navbar.css';
import logo from '../assets/logo.png';
import { useAuth } from '../contexts/AuthContext'; // Adjust the path as necessary
import { Link } from 'react-router-dom';

const Navbar = () => {
  const { loggedIn } = useAuth();

  return (
    <nav className="navbar">
      <div className="logo">
        <Link to='/'>
          <img src={logo} alt="Logo" />
        </Link>
      </div>
      <div className="title">
        <h1>DIGITALNI VODOMJER</h1>
      </div>
      <div className="links">
        {loggedIn ? (
          <Link to="/logout">Log out</Link>
        ) : (
          <Link to="/login">Log in</Link>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
