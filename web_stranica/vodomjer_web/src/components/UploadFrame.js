import React from 'react';
import '../assets/uploadframe.css';

const UploadFrame = ({ width, height, files }) => {
  return (
    <div className="frame-container">
      <div className="frame2" style={{ width, height }}>
        <div className="header">UPLOADANE DATOTEKE</div>
        <ul className="file-list">
          {files.map((file, index) => (
            <li key={index}>{file.name}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default UploadFrame;
