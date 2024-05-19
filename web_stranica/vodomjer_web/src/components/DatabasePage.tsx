import React, { useState, useEffect } from "react";
import axios from "axios";
import "../App.css";
import er_dijagram from '../assets/er_dijagram.png';
import { useDatabase } from '../contexts/DatabaseProvider';

function DatabasePage() {
    const [file, setFile] = useState<File | null>(null);
    const [msg, setMsg] = useState<string>("");
    const {
        databaseAvailable, 
        setDatabaseAvailable,
        uploadedFilePath, 
        setUploadedFilePath
    } = useDatabase();  // Use context

    // Effect to update message based on the availability of the database
    useEffect(() => {
        if (databaseAvailable) {
            setMsg("Database is uploaded and available.");
        } else {
            setMsg("Database is not uploaded.");
        }
    }, [databaseAvailable]);

    const handleUpload = async () => {
        if (!file) {
            setMsg("No file selected");
            return;
        }
        const formData = new FormData();
        formData.append('database', file);

        try {
            const response = await axios.post('/upload', formData, { withCredentials: true });
            if (response.data.success) {
                setMsg(response.data.success);
                setDatabaseAvailable(true);
                setUploadedFilePath(response.data.filename);  // Assume response contains the path or filename
            } else {
                setMsg(response.data.error);
            }
        } catch (error) {
            setMsg("Upload failed");
            console.error('Upload error:', error);
        }
    };

    const handleDownload = async () => {
        if (!databaseAvailable || !uploadedFilePath) {
            setMsg("No database available to download.");
            return;
        }
        try {
            const response = await axios.get(`/download`, { 
                responseType: 'blob', // Ensure the response type is set to 'blob'
                headers: {
                    'Content-Type': 'application/octet-stream', // This line might not be necessary
                }
            });
            if (response.status === 200) {
                const url = window.URL.createObjectURL(new Blob([response.data]));
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', uploadedFilePath); // Use the actual filename from the session if available
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link); // Clean up
                setMsg("Download successful.");
            } else {
                setMsg("Download failed: " + response.statusText);
            }
        } catch (error: any) {
            console.error('Download error:', error);
            setMsg("Download error: " + error.message);
        }
    };
    

    return (
        <div className="App">
            <div className="submit">
                <p>{msg}</p>
                <input type="file" onChange={(e) => {
                    if (e.target.files) {
                        setFile(e.target.files[0]);
                    }
                }} />
                <button onClick={handleUpload}>Upload</button>
                <button onClick={handleDownload} disabled={!databaseAvailable}>Download</button>
            </div>
            <div className="prozor">
                <img src={er_dijagram} alt="ER Diagram" style={{ maxWidth: '100%' }}/>
            </div>
        </div>
    );
}

export default DatabasePage;
