import React from 'react';
import '../assets/sidemenu.css';

const Sidemenu = () => {
  return (
    <div className="side-menu">
      <ul>
        <li><a href="/ucitavanje">Učitavanje datoteka vodomjera/bankovnih izvoda</a></li>
        <li><a href="/izvjestaj">Formiranje izvještaja</a></li>
        <li><a href="/slanje">Slanje izvještaja</a></li>
        <li><a href="/baza">Uvid u bazu podataka</a></li>
      </ul>
    </div>
  );
};

export default Sidemenu;
