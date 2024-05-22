import { useEffect, useState } from "react";
import { useAuth } from '../contexts/AuthContext';
import axios from "axios";

const LineChart = () => {
    //const [zgrade, setZgrade] = useState();
    const [zgrade, setZgrade] = useState(['prva', 'druga', 'treca']);

    useEffect(() => {
        const getZgrade = async () => {
            const result = await axios.get('/get_zgrade')
            .then(response => {
                console.log(response.data);
                //setZgrade(response.data);
            })
            .catch(error => console.error('Greska LineChart', error));
        }

        getZgrade();
    }, [zgrade]);

    ///////////////////////////////////////////////////////////////////////
    // kod koji sam koje se koristio za testiranje backenda- nije napravljen izbor godine i vraćanje podataka grafa na frontendu
    const [buildings, setBuildings] = useState([]);
    const [selectedBuilding, setSelectedBuilding] = useState('');
    const [users, setUsers] = useState([]);
    const [selectedUser, setSelectedUser] = useState('');

    useEffect(() => {
        const fetchData = async () => {
            try {
                const buildingsResponse = await axios.get('/get_zgrade');
                setBuildings(buildingsResponse.data.buildings || []);

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
    };
    ///////////////////////////////////////////////////////////////////////////////////////////
    return (
        <div>
            {"Izbornik koji se koristio kod testiranja"}
            <form onSubmit={handleSubmit}>
                <div>
                    <label>
                        Building:
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
                        User:
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
            </form>


            
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
