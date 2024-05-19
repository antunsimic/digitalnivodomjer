import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext'; // Ensure the correct path to your AuthContext

function LogoutPage() {
  const { setLoggedIn } = useAuth();  // Use setLoggedIn from AuthContext
  const navigate = useNavigate();

  useEffect(() => {
    const logoutTimeout = setTimeout(() => {
      // Call to backend endpoint for logout
      fetch('/logout', {
        method: 'GET',
        credentials: 'include', // Include cookies if using session-based authentication
      })
      .then(response => {
        if (response.ok) {
          return response.json();
        }
        throw new Error('Logout failed');
      })
      .then(data => {
        // If logout is successful
        if (data.success) {
          setLoggedIn(false);  // Update the AuthContext's loggedIn state
          navigate('/');  // Redirect to the home page
          //alert('Podaci izbrisani iz /login-backend/podaci.txt');
        } else {
          // Handle any errors that aren't related to network issues
          console.error('Logout failed with response:', data);
        }
      })
      .catch(error => {
        console.error('Logout error:', error);
      });
    }, 500);  // Delay to simulate network call

    return () => clearTimeout(logoutTimeout);  // Cleanup on component unmount
  }, [navigate, setLoggedIn]);  // Dependencies for useEffect

  return <h1>Logging out</h1>;
}

export default LogoutPage;

