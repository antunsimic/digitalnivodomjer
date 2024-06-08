import React from 'react';
import '../assets/createreport.css';

const CreateReport = () => {
  return (
    <div className="container">
      <div className="button-container">
        <button className="generate-button">GENERIRAJ IZVJEŠTAJ ZA VODOVOD</button>
        <button className="generate-button">GENERIRAJ IZVJEŠTAJ ZA ZGRADU</button>
      </div>
      <div className="generated-reports">
        <div className="reports-header">Napravljeni izvještaji</div>
        <div className="reports-list">
        </div>
      </div>
    </div>
  );
};

export default CreateReport;