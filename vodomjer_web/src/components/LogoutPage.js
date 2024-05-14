import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function LogoutPage({ setLoggedIn }) {
  const navigate = useNavigate();

  useEffect(() => {
    const logoutTimeout = setTimeout(() => {
      // Assuming you have a backend endpoint for logout at /logout
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
          // Assuming your backend returns success: true if logout is successful
          if (data.success) {
            setLoggedIn(false);
            navigate('/');
            // Display alert after successful logout
            alert('Podaci izbrisani iz /login-backend/podaci.txt');
          } else {
            // Handle error, if needed
          }
        })
        .catch(error => {
          console.error('Logout error:', error);
          // Handle error, if needed
        });
    }, 500); // Delay (da se vidi "Logging out...")

    return () => clearTimeout(logoutTimeout); // Cleanup function to clear the timeout if component unmounts
  }, [navigate, setLoggedIn]);

  return <h1>Logging out</h1>;
}

export default LogoutPage;
