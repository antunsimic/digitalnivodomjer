import React from 'react';
import '../assets/navbar.css';
import logo from '../assets/logo.png'

const Navbar = ({ loggedIn, setLoggedIn }) => {
  return (
    <nav className="navbar">
      <div className="logo">
        <a href='/'>
            <img src={logo} alt="Logo" />
        </a>
      </div>
      <div className="title">
        <h1>DIGITALNI VODOMJER</h1>
      </div>
      <div className="links">
        {loggedIn ? (
          <a href="/logout">Log out</a>
        ) : (
          <a href="/login">Log in</a>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
