import React from 'react';
import '../assets/navbar.css';
import logo from '../assets/logo.png'

const Navbar = () => {
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
        <a href="/login">Login</a>
        <a href="/register">Register</a>
      </div>
    </nav>
  );
};

export default Navbar;
