import {useState, useEffect} from "react";
import axios from "axios";
import "../App.css";
import er_dijagram from '../assets/er_dijagram.png' //import slike er dijagrama za prikaz unutar prozora

import { BrowserRouter as Router, Route, Routes, Link, useLocation } from 'react-router-dom';

function DatabasePage() {
    const [file, setFile] = useState<File | null>(null);
    const [msg, setMsg] = useState(" ");
    const [databaseAvailable, setDatabaseAvailable] = useState(false);

    //postavak indikatora pri loadanju stranice
    useEffect(() => {
        axios.get('/database_availability')
            .then(response => {
                setDatabaseAvailable(response.data.database_available);
            })
            .catch(error => {
                console.error('Error fetching database availability:', error);
            });
    }, []);


    // handle za upload sa strane frontenda
    function handleUpload(){
        if(!file){
            setMsg("No file selected");
            return;
        }

        const fd = new FormData();
        fd.append('database', file);

        setMsg("Uploading...");
        
        axios.post('/upload' , fd, {

        })
            .then(res =>{
                //setMsg("    Upload succesful");
                //povratne informacije s backenda
                if(res.data.success){
                    setMsg(res.data.success);
                    // postavi indikator na true ako je upload uspjesan
                    setDatabaseAvailable(true);
                }
                else if(res.data.error){
                    setMsg(res.data.error);
                }
                
                console.log(res);
            })
            .catch(err => {
                // u slucaju errora samog posta
                setMsg("    Upload failed");
                console.error(err);
            });
        
    }
// handle za pozivanje preuzimanja baze
    const handleDownload = () => {
        axios({
            url: '/download',
            method: 'GET',
            responseType: 'arraybuffer',
        }).then(response => {
            // Provjera ako je file
            if (response.headers['content-type'].indexOf('application/octet-stream') !== -1) {
                const url = window.URL.createObjectURL(new Blob([response.data]));
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', 'vodomjeri.db'); // Replace with your file name
                document.body.appendChild(link);
                link.click();
            } else {
                // ostali mogući odgovori (errori)
                console.error(response.data);
            }
        }).catch(error => {
            // error samog requesta
            console.error(error);
        });
    }

   

    // Brisanje po premjestanju na bilo koju stranicu unutar webapp i refreshanju
    const location = useLocation();
    useEffect(() => {
        const handleNavigate = () => {
            
            axios.delete('/delete')
                .then(() => {
                    console.log('Uploaded file deleted');
                })
                .catch(error => {
                    console.error('Error deleting uploaded file:', error);
                });
        };
        const cleanup = () => {
            handleNavigate();
        };
        return () => {
            cleanup();
        };
    }, [location]);

    // Brisanje po zatvaranju taba i refreshanju ali ne po promjeni stranice unutar webappa
    window.onbeforeunload = () => axios.delete('/delete');


    return(

         <div className="App">
            
            <div className = "submit">
            {databaseAvailable ? (
                <p>Database is uploaded and available.</p>
                ) : (
                <p>Database is not uploaded.</p>
             )}
            
             <input onChange={(e) => { 
                    const selectedFile = e.target.files && e.target.files[0];
                    if (selectedFile) {
                        setFile(selectedFile);
                    } else {
                        // Handle case where user cancels or clears file selection
                        setFile(null);
                    }
             }} type="file" />
                 <button type="submit" className= "btn btn-primary" onClick={handleUpload}>Upload</button>

                 <br></br>
                 <p>{msg && <span>{msg}</span>}</p>
                 <p>Baza mora biti formata kao u ER dijagramu</p>
             </div>


             <div className="prozor">
                 <p> </p>
                 <img src={er_dijagram} alt="ER DIJAGRAM BAZE PODATAKA" style={{ maxWidth: '100%' }}/>
             </div>
             <br></br><br></br>
             <div className="download">
                 <button type="button" className="btn btn-primary" onClick={handleDownload}>Download</button>
             </div>

          </div>
    );
}
export default DatabasePage;
