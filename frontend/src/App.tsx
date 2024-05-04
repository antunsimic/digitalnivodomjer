import {useState} from "react";
import axios from "axios";
import "./App.css";
import "./app.py"
import "./bazaPodatakaFunct.py"


function App(){
    const [file, setFile] = useState<File | null>(null);
    const [progress, setProgress] = useState({started:false, pc: 0});
    const [msg, setMsg] = useState(" ");

    function handleUpload(){
        if(!file){
            setMsg("No file selected");
            return;
        }

        const fd = new FormData();
        fd.append('database', file);

        setMsg("Uploading...");
        setProgress(prevState => {
            return {...prevState, started: true}
        })
        axios.post('/upload' , fd, {
           // onUploadProgress: (progressEvent) => {setProgress(prevState => {
           //     return  {...prevState, pc: progressEvent.progress*100};
           // } )},

        })
            .then(res =>{
                setMsg("    Upload succesful");
                console.log(res.data);
            })
            .catch(err => {
                setMsg("    Upload failed");
                console.error(err);
            });
    }
// dodano za povezivanje A
    const handleDownload = () => {
        axios.get('/download')
            .then(response => {
                setMsg("Sucecessful download")
            })
    }
// A
    return(

         <div className="App">

             <div className = "submit">
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

                 {progress.started && <progress max="100" value={progress.pc}>.</progress>}
                 {msg && <span>{msg}</span>}
             </div>



             <div className="prozor">
                 <p> </p>
             </div>

             <div className="download">
                 <button type="button" className="btn btn-primary" onClick={handleDownload}>Download</button>
             </div>



          </div>
    );
}
export default App;