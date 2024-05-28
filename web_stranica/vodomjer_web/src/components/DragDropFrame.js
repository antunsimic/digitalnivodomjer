import React, { useState } from 'react';
import '../assets/dragdropframe.css';

const DragDropFrame = ({ width, height, onFilesDropped, onButtonClick }) => {
  const [dragging, setDragging] = useState(false);

  const handleDragEnter = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragging(false);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragging(false);

    const files = Array.from(e.dataTransfer.files);
    const allowedExtensions = ['txt', 'xls', 'xlsx', 'otp'];
    const filteredFiles = files.filter(file => 
      allowedExtensions.includes(file.name.split('.').pop().toLowerCase())
    );

    onFilesDropped(filteredFiles);
  };

  return (
    <div className="frame-container">
      <div
        className={`frame ${dragging ? 'dragging' : ''}`}
        style={{ width, height }}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
      >
        DRAG AND DROP UPLOAD .TXT/.XLS/.XLSX/.OTP
      </div>
      <div className="button-container">
        <button className="button" onClick={onButtonClick}>
          Unos u bazu podataka
        </button>
      </div>
    </div>
  );
}

export default DragDropFrame;
