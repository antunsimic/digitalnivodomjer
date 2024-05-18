import React, { useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext'; // Make sure the path is correct
import axios from 'axios';

const AuthStatusChecker = () => {
    const { setLoggedIn } = useAuth(); // Use the hook to access setLoggedIn
    const location = useLocation();

    useEffect(() => {
        axios.get('/check-login-status', { withCredentials: true })
            .then(response => {
                console.log('Login status:', response.data.logged_in);
                setLoggedIn(response.data.logged_in);
            })
            .catch(error => console.error('Auth check failed:', error));
    }, [location, setLoggedIn]); // Include setLoggedIn in the dependency array

    return null; // Renders nothing, just handles login status
};

export default AuthStatusChecker;
