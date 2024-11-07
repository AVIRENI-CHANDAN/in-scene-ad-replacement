import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from './../AuthContext';
import styles from './NavigationBar.module.scss';

function NavBar() {
  const { isAuthenticated, logout } = useAuth();

  return (
    <nav className={styles.NavigationBar}>
      {isAuthenticated ? (
        // Post-login navigation items
        <>
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/profile">Profile</Link>
          <button onClick={logout}>Logout</button>
        </>
      ) : (
        // Pre-login navigation items
        <>
          <Link to="/login">Login</Link>
          <Link to="/signup">Sign Up</Link>
        </>
      )}
    </nav>
  );
}

export default NavBar;
