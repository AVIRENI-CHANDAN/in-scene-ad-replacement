import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './RegistrationPage.module.scss';

function RegistrationPage() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [verificationCode, setVerificationCode] = useState('');
  const [isRegistered, setIsRegistered] = useState(false);
  const [isVerified, setIsVerified] = useState(false);
  const navigate = useNavigate();

  const handleRegister = async () => {
    try {
      const response = await fetch('/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password }),
      });
      if (response.ok) {
        setIsRegistered(true);
      } else {
        console.error('Registration failed');
      }
    } catch (error) {
      console.error('Error during registration:', error);
    }
  };

  const handleVerifySignUp = async () => {
    try {
      const response = await fetch('/auth/verify_sign_up', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, code: verificationCode }),
      });
      if (response.ok) {
        setIsVerified(true);
      } else {
        console.error('Verification failed');
      }
    } catch (error) {
      console.error('Error during verification:', error);
    }
  };

  // Redirect to login if both registration and verification are successful
  if (isRegistered && isVerified) {
    navigate('/login');
  }

  return (
    <div className={styles.Register}>
      <h1>Register</h1>
      {isRegistered ?
        <div className={styles.FormSection}>
          <h2>Verify Your Account</h2>
          <label>Verification Code</label>
          <input type="text" value={verificationCode} onChange={(e) => setVerificationCode(e.target.value)} />
          <button className={styles.SubmitButton} onClick={handleVerifySignUp}>
            Verify
          </button>
        </div>
        :
        <div className={styles.FormSection}>
          <label>Username</label>
          <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />

          <label>Email</label>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />

          <label>Password</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />

          <button className={styles.SubmitButton} onClick={handleRegister}>
            Register
          </button>
        </div>}
    </div>
  );
}

export default RegistrationPage;
