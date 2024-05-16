import React from 'react';
import '../assets/uploadframe.css';

const Upload = ({ width, height }) => {
  return (
    <div className="frame-container">
      <div className="frame2" style={{ width, height }}>
        UPLOADANE DATOTEKE
      </div>
    </div>
  );
}

export default Upload;