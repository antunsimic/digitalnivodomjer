// LoginPage.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';  // Ensure axios is installed and imported
import { useAuth } from '../contexts/AuthContext'; // Correct the path if necessary

function LoginPage() {
  const { setLoggedIn } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [message, setMessage] = useState('');

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setEmail(name === 'email' ? value : email);
    setPassword(name === 'password' ? value : password);
  };

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post('/login', { email, password }, {
        headers: { 'Content-Type': 'application/json' },
        withCredentials: true
      });
      if (response.data.success) {
        setLoggedIn(true);
        navigate('/');
      } else {
        setMessage(response.data.message || 'Login failed');
      }
    } catch (error) {
      setMessage(error.response?.data?.error || "Login error");
      console.error('Error:', error);
    }
  };

  return (
    <div style={{ textAlign: 'center' }}>
      <h2>Log in</h2>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '1rem' }}>
          <label>Email address</label>
          <br />
          <input type="email" name="email" value={email} onChange={handleInputChange} />
        </div>
        <div style={{ marginBottom: '1rem' }}>
          <label>Password</label>
          <br />
          <input type={showPassword ? 'text' : 'password'} name="password" value={password} onChange={handleInputChange} />
          <button type="button" onClick={togglePasswordVisibility}>
            {showPassword ? 'Hide' : 'Show'} Password
          </button>
        </div>
        <button type="submit">Log in</button>
        {message && <div>{message}</div>}
      </form>
    </div>
  );
}

export default LoginPage;
