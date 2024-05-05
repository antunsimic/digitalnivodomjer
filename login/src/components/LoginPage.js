import React from 'react';

class LoginPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      showPassword: false
    };
  }

  togglePasswordVisibility = () => {
    this.setState(prevState => ({
      showPassword: !prevState.showPassword
    }));
  }

  render() {
    return (
      <div style={{ textAlign: 'center' }}>
        <h2>Log in</h2>
        <form>
          <div style={{ marginBottom: '1rem' }}>
            <label style={{ marginRight: '1rem' }}>Email address</label>
            <br />
            <input type="email" />
          </div>
          <div style={{ marginBottom: '1rem' }}>
            <label style={{ marginRight: '1rem' }}>Password</label>
            <br />
            <input type={this.state.showPassword ? 'text' : 'password'} />
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
