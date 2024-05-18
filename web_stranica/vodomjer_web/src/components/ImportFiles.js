import React, { useState } from 'react';
import DragDropFrame from './DragDropFrame';
import UploadFrame from './UploadFrame';
import '../assets/importfiles.css';  // Import the new CSS file

const ImportFiles = () => {
  const [files, setFiles] = useState([]);

  const handleFilesDropped = (droppedFiles) => {
    setFiles(droppedFiles);
  };

  const handleButtonClick = async () => {
    if (files.length === 0) {
      alert('Nema datoteka za unos');
      return;
    }

    const formData = new FormData();
    files.forEach(file => formData.append('files', file));

    try {
      const response = await fetch('/upload-izvjestaj', {
        method: 'POST',
        body: formData
      });

      if (response.ok) {
        alert('Datoteke uspjesno unesene');
      } else {
        console.error('Greska prilikom unosa:', response.statusText);
        alert('Greska prilikom unosa');
      }
    } catch (error) {
      console.error('Greska prilikom unosa:', error);
      alert('Greska prilikom unosa');
    }
  };

  return (
    <div className="import-files-container">
      <div className="dragdrop-container">
        <DragDropFrame width="800px" height="500px" onFilesDropped={handleFilesDropped} onButtonClick={handleButtonClick} />
      </div>
      <UploadFrame width="300px" height="700px" files={files} />
    </div>
  );
}

export default ImportFiles;
