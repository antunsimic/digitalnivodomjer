import React from 'react';
import '../assets/dragdropframe.css';

const DragDrop = ({ width, height }) => {
  return (
    <div className="frame-container">
      <div className="frame" style={{ width, height }}>
        DRAG AND DROP UPLOAD .TXT/.XLS/.XLSX/.OTP
      </div>
      <div className="button-container">
        <button className="button">Unos u bazu podataka</button>
      </div>
    </div>
  );
}

export default DragDrop;
