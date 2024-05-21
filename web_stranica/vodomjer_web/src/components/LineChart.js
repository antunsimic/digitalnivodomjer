import { useEffect, useState } from "react";
import { useAuth } from '../contexts/AuthContext';
import axios from "axios";

const LineChart = () => {
    //const [zgrade, setZgrade] = useState();
    const [zgrade, setZgrade] = useState(['prva', 'druga', 'treca']);

    useEffect(() => {
        const getZgrade = async () => {
            const result = await axios.get('http://localhost:5000/get_zgrade')
            .then(response => {
                console.log(response.data);
                //setZgrade(response.data);
            })
            .catch(error => console.error('Greska LineChart', error));
        }

        getZgrade();
    }, [zgrade]);

    return (
        <div>
            <div className="dropdown">
                <select>
                    <option value="">Izaberite zgradu</option>
                    {zgrade.map((zgrada, index) => (
                            <option key={index} value={zgrada}>{zgrada}</option>
                        ))}
                </select>
                <select>
                    <option value="">Izaberite korisnika</option>
                        {zgrade.map((zgrada, index) => (
                            <option key={index} value={zgrada}>{zgrada}</option>
                        ))}
                </select>
                <select>
                    <option value="">Izaberite godinu</option>
                        {zgrade.map((zgrada, index) => (
                            <option key={index} value={zgrada}>{zgrada}</option>
                        ))}
                </select>
            </div>
        </div>
    );
}

export default LineChart;