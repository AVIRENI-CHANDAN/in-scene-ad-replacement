import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthContext';
import styles from './RegistrationPage.module.scss';

function RegistrationPage() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [verifyPassword, setVerifyPassword] = useState('');
  const [verificationCode, setVerificationCode] = useState('');
  const [isRegistered, setIsRegistered] = useState(false);
  const [isVerified, setIsVerified] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [username_input_active, setUsernameInputActive] = useState(false);
  const [email_input_active, setEmailInputActive] = useState(false);
  const [password_input_active, setPasswordInputActive] = useState(false);
  const [verify_password_input_active, setVerifyPasswordInputActive] = useState(false);
  const [verification_input_active, setVerificationInputActive] = useState(false);
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  // Clear error message after 3 seconds
  useEffect(() => {
    if (errorMessage) {
      const timeout = setTimeout(() => {
        setErrorMessage('');
      }, 3000);
      return () => clearTimeout(timeout); // Cleanup timeout on unmount or errorMessage change
    }
  }, [errorMessage]);

  useEffect(() => {
    if (isAuthenticated) {
      navigate('/dashboard');
    }
  }, [isAuthenticated, navigate]);

  useEffect(() => {
    if (isRegistered && isVerified) {
      navigate('/login');
    }
  }, [isRegistered, isVerified, navigate]);

  const handleRegister = async (event) => {
    event.preventDefault();
    setErrorMessage('');

    // Validation for empty fields
    if (!username.trim()) {
      setErrorMessage('Username cannot be empty.');
      return;
    }
    if (!email.trim()) {
      setErrorMessage('Email cannot be empty.');
      return;
    }
    if (!password.trim()) {
      setErrorMessage('Password cannot be empty.');
      return;
    }
    if (password !== verifyPassword) {
      setErrorMessage('Passwords do not match.');
      return;
    }

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

  const handleVerifySignUp = async (event) => {
    event.preventDefault();
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

  const handleResendVerification = async (event) => {
    event.preventDefault();
    setErrorMessage('');
    try {
      const response = await fetch('/auth/resend-verification', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username }),
      });
      if (!response.ok) {
        const errorData = await response.json();
        setErrorMessage(errorData.error || 'Request failed');
      }
    } catch (error) {
      console.error('Error during request:', error);
      setErrorMessage('An error occurred during request. Please try again.');
    }
  }

  return (
    <div className={styles.Register}>
      <div className={styles.RegistrationContainer}>
        <div className={styles.LogoTitleWrapper}>
          <div className={styles.Box}>
            <div className={styles.Logo}>
              <img src="https://gyrus.ai/assets/website_assets/assets/images/demoPageAssets/gyrus-blue.png" alt="Logo" />
            </div>
            <div className={styles.Title}>
              ISAR 2D Demo
            </div>
            <div className={styles.MediaLinkWrapper}>
              <div className={styles.MediaLinkBox}>
                <img src='https://gyrus.ai/assets/videodemoassets/facebook.png' alt='Facebook' />
              </div>
              <div className={styles.MediaLinkBox}>
                <img src='https://gyrus.ai/assets/videodemoassets/youtube.png' alt='Youtube' />
              </div>
              <div className={styles.MediaLinkBox}>
                <img src='https://gyrus.ai/assets/videodemoassets/X_logo_2023_(white).png' alt='X' />
              </div>
              <div className={styles.MediaLinkBox}>
                <img src='https://gyrus.ai/assets/videodemoassets/linkedin.png' alt='LinkedIn' />
              </div>
            </div>
          </div>
        </div>

        <div className={styles.RegistrationWrapper}>
          <h1>Welcome to Gyrus AI</h1>
          {errorMessage && <p className={styles.ErrorMessage}>{errorMessage}</p>}
          {isRegistered ? (
            <form className={styles.FormSection} onSubmit={handleVerifySignUp}>
              <h2>Verify Your Account</h2>
              <div className={styles.FormGroup}>
                <label className={`${verification_input_active ? styles.TopLabel : ''}`}>Verification Code</label>
                <input
                  type="text"
                  value={verificationCode}
                  onChange={(e) => { setVerificationCode(e.target.value); setVerificationInputActive(e.target.value !== ''); }}
                  required
                />
              </div>
              <button className={styles.SubmitButton} type='submit'>
                Verify
              </button>
              <div onClick={handleResendVerification} className={styles.ResendCodeLink}>Resend code</div>
            </form>
          ) : (
            <form className={styles.FormSection} onSubmit={handleRegister}>
              <div className={styles.FormGroup}>
                <label className={`${username_input_active ? styles.TopLabel : ''}`}>Username</label>
                <input
                  type="text"
                  value={username}
                  onChange={(e) => { setUsername(e.target.value); setUsernameInputActive(e.target.value !== ''); }}
                  required
                />
              </div>
              <div className={styles.FormGroup}>
                <label className={`${email_input_active ? styles.TopLabel : ''}`}>Email</label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => { setEmail(e.target.value); setEmailInputActive(e.target.value !== ''); }}
                  required
                />
              </div>
              <div className={styles.FormGroup}>
                <label className={`${password_input_active ? styles.TopLabel : ''}`}>Password</label>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => { setPassword(e.target.value); setPasswordInputActive(e.target.value !== ''); }}
                  required
                />
              </div>
              <div className={styles.FormGroup}>
                <label className={`${verify_password_input_active ? styles.TopLabel : ''}`}>Verify Password</label>
                <input
                  type="password"
                  value={verifyPassword}
                  onChange={(e) => { setVerifyPassword(e.target.value); setVerifyPasswordInputActive(e.target.value !== ''); }}
                  required
                />
              </div>
              <button className={styles.SubmitButton} type='submit'>
                Register
              </button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}

export default RegistrationPage;
