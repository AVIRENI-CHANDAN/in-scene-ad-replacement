import React from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './NotFound.module.scss';

function NotFound() {
  const navigate = useNavigate();

  const handleGoHome = () => {
    navigate('/');
  };

  return (
    <div className={styles.NotFound}>
      <h1>404</h1>
      <p>Oops! The page you are looking for does not exist.</p>

      <button className={styles.GoHomeButton} onClick={handleGoHome}>
        Go Home
      </button>
    </div>
  );
}

export default NotFound;
