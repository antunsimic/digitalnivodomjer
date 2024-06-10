import React, { useState } from 'react';
import '../assets/createreport.css';

const CreateReport = () => {
  const [reportFiles, setReportFiles] = useState([]);
  const [lastClick, setLastClick] = useState(''); // State to track the last clicked button

  const generirajVodovod = async () => {
    try {
      const response = await fetch('/generiraj-izvjestaj-za-vodovod', {
        method: 'POST'
      });
      const result = await response.json();
      alert(result.message);
    } catch (error) {
      console.error('Greska prilikom generiranja izvjestaja za vodovod:', error);
    }
  };

  const getVodovod = async () => {
    try {
      const response = await fetch('/get-izvjestaj-za-vodovod', {
        method: 'GET'
      });
      const result = await response.json();
      setReportFiles(result); // Assuming result is a list of file names
    } catch (error) {
      console.error('Greska prilikom dohvacanja izvjestaja:', error);
    }
  };

  const handleVodovodClick = async () => {
    await generirajVodovod();
    await getVodovod();
    setLastClick('vodovod'); // Update the last click state
  };

  const generirajZgrada = async () => {
    try {
      const response = await fetch('/generiraj-izvjestaj-za-zgradu', {
        method: 'POST'
      });
      const result = await response.json(); 
      alert(result.message);
    } catch (error) {
      console.error('Greska prilikom generiranja izvjestaja za zgradu:', error);
    }
  };

  const getZgrada = async () => {
    try {
      const response = await fetch('/get-izvjestaj-za-zgradu', {
        method: 'GET'
      });
      const result = await response.json();
      setReportFiles(result); // Assuming result is a list of file names
    } catch (error) {
      console.error('Greska prilikom dohvacanja izvjestaja:', error);
    }
  };

  const handleZgradaClick = async () => {
    await generirajZgrada();
    await getZgrada();
    setLastClick('zgrada'); // Update the last click state
  };

  const handleDownload = async () => {
    try {
      let downloadUrl = '';
      let fileName = '';

      if (lastClick === 'vodovod') {
        downloadUrl = '/download-vodovod';
        fileName = 'vodovod.zip';
      } else if (lastClick === 'zgrada') {
        downloadUrl = '/download-zgrada';
        fileName = 'zgrade.zip';
      } else {
        alert('Nijedan izvještaj nije generiran');
        return;
      }

      const response = await fetch(downloadUrl, {
        method: 'GET'
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const blob = await response.blob();
      const blobUrl = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = blobUrl;
      a.download = fileName;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(blobUrl);
    } catch (error) {
      console.error('Greska prilikom preuzimanja izvjestaja:', error);
    }
  };

  return (
    <div className="container">
      <div className="button-container">
        <button className="generate-button" onClick={handleVodovodClick}>GENERIRAJ IZVJEŠTAJ ZA VODOVOD</button>
        <button className="generate-button" onClick={handleZgradaClick}>GENERIRAJ IZVJEŠTAJ ZA ZGRADU</button>
      </div>
      <div className="generated-reports">
        <div className="reports-header">Napravljeni izvještaji</div>
        <div className="reports-list">
          {reportFiles.map((file, index) => (
            <div key={index}>{file}</div>
          ))}
        </div>
      </div>
      <div className="download-button-container">
        <button className="download-button" onClick={handleDownload}>PREUZIMANJE</button>
      </div>
    </div>
  );
};

export default CreateReport;
