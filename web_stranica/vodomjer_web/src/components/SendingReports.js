import { useEffect, useState } from 'react'
import mailIcon from '../assets/mail.png'
import '../assets/reports.css'
import axios from 'axios'

const SendingReports = () => {

    const [reports, setReports] = useState([]);
    const [emailStatus, setEmailStatus] = useState([]);
    const [pollingInterval, setPollingInterval] = useState(null);

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

    const startPolling = () => {
        // Namjesti polling interval
        const interval = setInterval(fetchEmailStatus, 1000); // Poll every second
        setPollingInterval(interval);
    };

    const stopPolling = () => {
        // počisti polling
        clearInterval(pollingInterval);
        setPollingInterval(null);
        //const interval = setInterval(fetchEmailStatus, 100000); // Poll every second
        //setPollingInterval(interval);
    };

    // dohvati status emaila za prikaz ispod gumba - kontrolira se polling intervalom
    const fetchEmailStatus = async () => {
        try {
            const statusResponse = await axios.get('/email_status');
            setEmailStatus(statusResponse.data || []);
        } catch (error) {
            console.error('Error fetching email status:', error);
        }
    };

    const handleSending = async () => {
        console.log('Sending reports...');

        try {
            // početak polinga email statusa
            startPolling();

            // slanje emaila
            await axios.get('/send_emails');

            // delay prije kraja pollinga kako bi stigla i zadnja poruka
            await new Promise(resolve => setTimeout(resolve, 1000));

            // kraj polinga NE RADI - ako otkriješ kako napravit
            stopPolling();
        } catch (error) {
            console.error('Error sending reports:', error);
        }
    };

    


    return (
        <div className='report-container'>
            <div className='reports'>
                Izvještaji:
                {reports.map((report, index) => (
                    <div key={index}>{report}</div>
                ))}
            </div>
            <button onClick={handleSending}>
                <img width={50} height={50} src={mailIcon} alt="Send Reports" />
            </button>
            <div className='send-info'>
                Status slanja izvještaja:
                {emailStatus.map((status, index) => (
                    <div key={index}>{status}</div>
                ))}
            </div>
        </div>
    );
};

export default SendingReports;
