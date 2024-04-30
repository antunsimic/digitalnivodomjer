import React from 'react';
import '../assets/sidemenu.css';

const Sidemenu = () => {
  return (
    <div className="side-menu">
      <ul>
        <li><a href="/">Učitavanje datoteka vodomjera/bankovnih izvoda</a></li>
        <li><a href="/about">Formiranje izvještaja</a></li>
        <li><a href="/contact">Slanje izvještaja</a></li>
        <li><a href="/contact">Uvid u bazu podataka</a></li>
      </ul>
    </div>
  );
};

export default Sidemenu;
