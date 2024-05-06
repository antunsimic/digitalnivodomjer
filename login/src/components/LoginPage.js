import React from 'react';

class LoginPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      showPassword: false,
      email: '',
      password: ''
    };
  }

  togglePasswordVisibility = () => {
    this.setState(prevState => ({
      showPassword: !prevState.showPassword
    }));
  }

  handleInputChange = (event) => {
    const { name, value } = event.target;
    this.setState({ [name]: value });
  }

  handleSubmit = (event) => {
    event.preventDefault();

    // Fetch login API endpoint with POST method
    fetch('/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email: this.state.email,
        password: this.state.password
      })
    })
    .then(response => response.json())
    .then(data => {
      // Handle response from server (e.g., show success/failure message)
      console.log(data);
    })
    .catch(error => {
      // Handle error
      console.error('Error:', error);
    });
  }

  render() {
    return (
      <div style={{ textAlign: 'center' }}>
        <h2>Log in</h2>
        <form onSubmit={this.handleSubmit}>
          <div style={{ marginBottom: '1rem' }}>
            <label style={{ marginRight: '1rem' }}>Email address</label>
            <br />
            <input type="email" name="email" value={this.state.email} onChange={this.handleInputChange} />
          </div>
          <div style={{ marginBottom: '1rem' }}>
            <label style={{ marginRight: '1rem' }}>Password</label>
            <br />
            <input type={this.state.showPassword ? 'text' : 'password'} name="password" value={this.state.password} onChange={this.handleInputChange} />
            <button type="button" onClick={this.togglePasswordVisibility}>
              {this.state.showPassword ? 'Hide' : 'Show'} Password
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
}

export default LoginPage;
