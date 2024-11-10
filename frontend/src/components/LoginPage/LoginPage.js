import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthContext';
import styles from './LoginPage.module.scss';

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const { isAuthenticated, login } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (isAuthenticated) {
      navigate('/dashboard'); // Redirect to dashboard if already authenticated
    }
  }, [isAuthenticated, navigate]);

  const handleLogin = async (event) => {
    event.preventDefault();

    if (!username || !password) {
      setErrorMessage('Please fill in all fields');
      return;
    }

    if (username.length < 5 || password.length < 5) {
      setErrorMessage('Email and password must be at least 5 characters long');
      return;
    }

    try {
      const payload = { username, password };
      const response = await fetch('/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
        credentials: 'include',
      });

      if (response.ok) {
        login(); // Call login() to update isAuthenticated in AuthContext
        navigate('/dashboard'); // Navigate to dashboard only after successful login
      } else {
        let errorData;
        try {
            errorData = await response.json();
        } catch (e) {
            errorData = { error: 'Unable to process server response' };
        }
        setErrorMessage(errorData.error || 'Login failed');
      }
    } catch (error) {
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

        <button className={styles.SubmitButton} type="submit">
          Login
        </button>
      </form>
    </div>
  );
}

export default LoginPage;
