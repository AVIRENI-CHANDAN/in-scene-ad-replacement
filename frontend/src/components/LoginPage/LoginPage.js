import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthContext';
import styles from './LoginPage.module.scss';

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [username_input_active, setUsernameInputActive] = useState(false);
  const [password_input_active, setPasswordInputActive] = useState(false);
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

  const handleShowPassword = () => {
    console.log("Triggered the type change");
    setShowPassword(!showPassword);
  }

  return (
    <div className={styles.Login}>
      <div className={styles.LoginContainer}>
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

        <div className={styles.LoginWrapper}>
          <h1>Hello,Welcome to Gyrus AI
          </h1>
          <form className={styles.FormSection} onSubmit={handleLogin}>
            {errorMessage && <p className={styles.ErrorMessage}>{errorMessage}</p>}
            <div className={styles.FormGroup}>
              <label className={`${username_input_active ? styles.TopLabel : ''}`}>Username</label>
              <input
                type="text"
                value={username}
                onChange={(e) => { setUsername(e.target.value); setUsernameInputActive(e.target.value !== '') }}
                required
              />
              <div className={styles.Icon}>
                <i className='fas fa-user'></i>
              </div>
            </div>
            <div className={styles.FormGroup}>
              <label className={`${password_input_active ? styles.TopLabel : ''}`}>Password</label>
              <input
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={(e) => { setPassword(e.target.value); setPasswordInputActive(e.target.value !== '') }}
                required
              />
              <div className={styles.Icon}>
                <i className={`fas ${showPassword ? 'fa-eye-slash' : 'fa-eye'} ${styles.EyeIcon}`} onClick={handleShowPassword}></i>
              </div>
            </div>
            <div className={styles.FormGroup}>
              <Link to='forgot-password' className={styles.ForgotPasswordBtn}>Forgot Password?</Link>
            </div>
            <button className={styles.SubmitButton} type="submit">
              Sign In
            </button>
          </form>
          <div className={styles.RegistrationDirectSection}>Don't have a account? please <Link to='/signup' className={styles.RegistrationDirectLink}>Sign-up</Link></div>
        </div >
      </div>
    </div >
  );
}

export default LoginPage;
