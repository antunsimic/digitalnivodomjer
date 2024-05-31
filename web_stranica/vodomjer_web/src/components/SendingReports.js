import { useEffect, useState } from 'react'
import mailIcon from '../assets/mail.png'
import '../assets/reports.css'
import axios from 'axios'

const SendingReports = () => {

    const [reports, setReports] = useState([]);
    const [response, setResponse] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const reportsResponse = await axios.get('/reports');
                setReports(reportsResponse.data || []);
            } catch (error) {
                console.error('Error fetching reports for sending:', error);
            }
        };

        fetchData();
    }, []);

    const handleSending = () => {
        console.log('test buttona');

        const fetchData = async () => {
            try {
                const sentResponse = await axios.get('/send');
                setResponse(sentResponse.data || []);
            } catch (error) {
                console.error('Error sending reports:', error);
            }
        };

        fetchData();
    }

    return (
        <div className='report-container'>
            <div className='reports'>
                izvjestaji
                {reports}
            </div>
            <button onClick={handleSending}>
                <img width={50} height={50} src={mailIcon}></img>
            </button>
            <div className='send-info'>
                info o izvjestajima
                {response}
            </div>
        </div>
    )
}

export default SendingReports;