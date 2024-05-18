// src/contexts/AuthContext.js
import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext({});

export const AuthProvider = ({ children }) => {
  const [loggedIn, setLoggedIn] = useState(false);

  useEffect(() => {
    const fetchLoginStatus = async () => {
      try {
        const response = await axios.get('/check-login-status', { withCredentials: true });
        setLoggedIn(response.data.logged_in);
      } catch (error) {
        console.error('Failed to fetch login status:', error);
      }
    };

    fetchLoginStatus();
  }, []);

  return (
    <AuthContext.Provider value={{ loggedIn, setLoggedIn }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
