import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './LoginPage.module.scss';

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (event) => {
    event.preventDefault(); // Prevent the default form submission behavior
    if (!username || username.length < 3) {
      setErrorMessage('Username must be at least 3 characters');
      return;
    }
    if (!password || password.length < 8) {
      setErrorMessage('Password must be at least 8 characters');
      return;
    }
    try {
      const payload = { username, password };

      const response = await fetch('/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('id_token', data.id_token);
        localStorage.setItem('refresh_token', data.refresh_token);
        navigate('/dashboard');
      } else {
        const errorText = await response.text(); // Get the raw response text

        try {
          const errorData = JSON.parse(errorText); // Attempt to parse JSON if possible
          setErrorMessage(errorData.error || 'Login failed');
        } catch {
          setErrorMessage('An unexpected error occurred.'); // Fallback for non-JSON responses
        }
        console.error('Error during login:', errorText);
      }
    } catch (error) {
      console.error('Error during login:', error);
      setErrorMessage('An error occurred during login. Please try again.');
    }
  };


  return (
    <div className={styles.Login}>
      <h1>Login</h1>
      <form className={styles.FormSection} onSubmit={handleLogin}>
        {errorMessage && <p className={styles.ErrorMessage}>{errorMessage}</p>}

        <label>Username</label>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />

        <label>Password</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button className={styles.SubmitButton}>
          Login
        </button>
      </form>
    </div>
  );
}

export default LoginPage;
