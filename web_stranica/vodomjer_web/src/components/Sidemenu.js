import React from 'react';
import '../assets/sidemenu.css';
import { Link } from 'react-router-dom'; // Import Link from react-router-dom

const Sidemenu = () => {
  return (
    <div className="side-menu">
      <ul>
        <li><Link to="/ucitavanje">Učitavanje datoteka vodomjera/bankovnih izvoda</Link></li>
        <li><Link to="/izvjestaj">Formiranje izvještaja</Link></li>
        <li><Link to="/slanje">Slanje izvještaja</Link></li>
        <li><Link to="/baza">Uvid u bazu podataka</Link></li>
      </ul>
    </div>
  );
};

export default Sidemenu;
