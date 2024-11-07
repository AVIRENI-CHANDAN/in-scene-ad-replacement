import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from './../AuthContext';
import styles from './NavigationBar.module.scss';

function NavBar() {
  const { isAuthenticated, logout } = useAuth();

  return (
    <header className={styles.Header}>
      <Link to="/" className={styles.LogoContainer}>
        <div className={styles.LogoWrapper}>
          <img src="/g.svg" alt='G logo Error' className={styles.Logo} />
        </div>
      </Link>
      <nav className={styles.NavigationBar}>
        <div className={styles.ActionButtons}>
          {isAuthenticated ? (
            // Post-login navigation items
            <>
              <Link to="/dashboard" className={styles.ActionButton}>Dashboard</Link>
              <Link to="/profile" className={styles.ActionButton}>Profile</Link>
              <button onClick={logout} className={styles.LogoutActionButton}>Logout</button>
            </>
          ) : (
            // Pre-login navigation items
            <>
              <Link to="/login" className={styles.ActionButton}>Login</Link>
              <Link to="/signup" className={styles.ActionButton}>Sign Up</Link>
            </>
          )}
        </div>
      </nav>
    </header>
  );
}

export default NavBar;
