import { useEffect, useState } from "react";
import { useAuth } from '../contexts/AuthContext';
import axios from "axios";
import Graph from "./Graph";

const LineChart = () => {

    ///////////////////////////////////////////////////////////////////////
    // kod koji sam koje se koristio za testiranje backenda- nije napravljen izbor godine i vraćanje podataka grafa na frontendu
    const [buildings, setBuildings] = useState([]);
    const [selectedBuilding, setSelectedBuilding] = useState('');
    const [users, setUsers] = useState([]);
    const [selectedUser, setSelectedUser] = useState('');
    //const [years, setYears] = useState(['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']);
    const [years, setYears] = useState([]);
    const [selectedYear, setSelectedYear] = useState('');
    const [graphData, setGraphData] = useState([]);
    const [datumi, setDatumi] = useState([]);
    const [potrosnja, setPotrosnja] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const buildingsResponse = await axios.get('/get_zgrade');
                const yearsResponse = await axios.get('/get_godine');
                setBuildings(buildingsResponse.data.buildings || []);
                setYears(yearsResponse.data.years || []);
            } catch (error) {
                console.error('Error fetching buildings or years:', error);
            }
        };

        fetchData();
    }, []);

    const handleBuildingChange = async (buildingId) => {
        // kade se u form promijeni zgrada vracaju se korisnici vezani za tu zgradu
        setSelectedBuilding(buildingId);
        setSelectedUser(''); 

        try {
            const usersResponse = await axios.get('/get_korisnici', {
                params: { selected_building: buildingId }
            });
            setUsers(usersResponse.data.users || []);
        } catch (error) {
            console.error('Error fetching users:', error);
        }
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        // tu bi trebao ic kod za /potrosnja
        try {
            const graphResponse = await axios.get('/potrosnja', {
                params: { 
                    building: selectedBuilding,
                    user: selectedUser,
                    year: selectedYear
                }
            });
            setGraphData(graphResponse.data.consumption || []);
        } catch (error) {
            console.error('Error fetching graph data:', error);
        }
    };
    ///////////////////////////////////////////////////////////////////////////////////////////
    return (
        <div>            
            <div className="dropdown">
                
                <form onSubmit={handleSubmit}>
                    <div>
                        <label>
                            Zgrada:
                            <select value={selectedBuilding} onChange={(e) => handleBuildingChange(e.target.value)}>
                                <option value="">Select a building</option>
                                {buildings.map((building) => (
                                    <option key={building.id} value={building.id}>
                                        {building.ulica}, {building.mjesto}
                                    </option>
                                ))}
                            </select>
                        </label>
                    </div>
                    <div>
                        <label>
                            Korisnik:
                            <select value={selectedUser} onChange={(e) => setSelectedUser(e.target.value)}>
                                <option value="">Select a user</option>
                                {users.map((user) => (
                                    <option key={user.id} value={user.id}>
                                        {user.ime} {user.prezime}
                                    </option>
                                ))}
                            </select>
                        </label>
                    </div>
                    <div>
                        <label>
                            Godina: 
                            <select value={selectedYear} onChange={(e) => setSelectedYear(e.target.value)}>
                                <option value="">Select a year</option>
                                {years.map((year) => (
                                    <option key={year.id} value={year.id}>
                                        {year}
                                    </option>
                                ))}
                            </select>
                        </label>
                    </div>
                    <button type="submit">Potvrdi</button>
                </form>
            </div>
            <div>
                {typeof graphData !== '[]' && <Graph data={graphData} />}
            </div>
        </div>
        
    );
}

export default LineChart;
