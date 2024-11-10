import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthContext';
import styles from './RegistrationPage.module.scss';

function RegistrationPage() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [verificationCode, setVerificationCode] = useState('');
  const [isRegistered, setIsRegistered] = useState(false);
  const [isVerified, setIsVerified] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const { isAuthenticated } = useAuth(); // Access authentication state
  const navigate = useNavigate();

  // Redirect to dashboard if user is already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      navigate('/dashboard');
    }
  }, [isAuthenticated, navigate]);

  // Navigate to login after both registration and verification are successful
  useEffect(() => {
    if (isRegistered && isVerified) {
      navigate('/login');
    }
  }, [isRegistered, isVerified, navigate]);

  const handleRegister = async () => {
    setErrorMessage('');
    try {
      const response = await fetch('/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password }),
      });
      if (response.ok) {
        setIsRegistered(true);
      } else {
        const errorData = await response.json();
        setErrorMessage(errorData.error || 'Registration failed');
      }
    } catch (error) {
      console.error('Error during registration:', error);
      setErrorMessage('An error occurred during registration. Please try again.');
    }
  };

  const handleVerifySignUp = async () => {
    setErrorMessage('');
    try {
      const response = await fetch('/auth/verify_sign_up', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, code: verificationCode }),
      });
      if (response.ok) {
        setIsVerified(true);
      } else {
        const errorData = await response.json();
        setErrorMessage(errorData.error || 'Verification failed');
      }
    } catch (error) {
      console.error('Error during verification:', error);
      setErrorMessage('An error occurred during verification. Please try again.');
    }
  };

  return (
    <div className={styles.Register}>
      <h1>Register</h1>
      {errorMessage && <p className={styles.ErrorMessage}>{errorMessage}</p>}
      {isRegistered ? (
        <div className={styles.FormSection}>
          <h2>Verify Your Account</h2>
          <label>Verification Code</label>
          <input
            type="text"
            value={verificationCode}
            onChange={(e) => setVerificationCode(e.target.value)}
            required
          />
          <button className={styles.SubmitButton} onClick={handleVerifySignUp}>
            Verify
          </button>
        </div>
      ) : (
        <div className={styles.FormSection}>
          <label>Username</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <label>Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button className={styles.SubmitButton} onClick={handleRegister}>
            Register
          </button>
        </div>
      )}
    </div>
  );
}

export default RegistrationPage;
