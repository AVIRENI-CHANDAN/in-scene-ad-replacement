import React from 'react';
import { useAuth } from './../AuthContext';

function NavBar() {
  const { isAuthenticated, logout } = useAuth();

  return (
    <nav>
      {isAuthenticated ? (
        // Post-login navigation items
        <>
          <a href="/dashboard">Dashboard</a>
          <a href="/profile">Profile</a>
          <button onClick={logout}>Logout</button>
        </>
      ) : (
        // Pre-login navigation items
        <>
          <a href="/login">Login</a>
          <a href="/signup">Sign Up</a>
        </>
      )}
    </nav>
  );
}

export default NavBar;
