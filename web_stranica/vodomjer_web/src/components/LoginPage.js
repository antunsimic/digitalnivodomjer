import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function LoginPage({ setLoggedIn }) {
  const [showPassword, setShowPassword] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const togglePasswordVisibility = () => {
    setShowPassword(prevState => !prevState);
  }

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    if (name === 'email') setEmail(value);
    if (name === 'password') setPassword(value);
  }

  const handleSubmit = (event) => {
    event.preventDefault();

    // Fetch login API endpoint with POST method
    fetch('/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email: email,
        password: password
      })
    })
    .then(response => response.json())
    .then(data => {
      // Handle response from server (e.g., show success/failure message)
      console.log(data);
      setLoggedIn(true);
      console.log('Logged in: ', setLoggedIn);
      navigate('/');
      // Display alert after successful login
      alert('Podaci spremljeni u /login-backend/podaci.txt');
    })
    .catch(error => {
      // Handle error
      console.error('Error:', error);
    });
  }

  return (
    <div style={{ textAlign: 'center' }}>
      <h2>Log in</h2>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '1rem' }}>
          <label style={{ marginRight: '1rem' }}>Email address</label>
          <br />
          <input type="email" name="email" value={email} onChange={handleInputChange} />
        </div>
        <div style={{ marginBottom: '1rem' }}>
          <label style={{ marginRight: '1rem' }}>Password</label>
          <br />
          <input type={showPassword ? 'text' : 'password'} name="password" value={password} onChange={handleInputChange} />
          <button type="button" onClick={togglePasswordVisibility}>
            {showPassword ? 'Hide' : 'Show'} Password
          </button>
        </div>
        <button type="submit">Log in</button>
        <div>
          Ako ne znate što je Google App Password ili je još niste postavili, više informacija možete pronaći <a href="https://support.google.com/accounts/answer/185833?hl=en">ovdje.</a>
        </div>
      </form>
    </div>
  );
}

export default LoginPage;
