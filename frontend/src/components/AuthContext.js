// AuthContext.js
import React, { createContext, useContext, useEffect, useState } from 'react';

// Create a Context for the authentication state
const AuthContext = createContext();

// AuthProvider component to wrap around the parts of the app that need access to auth state
export function AuthProvider({ children }) {
    const [isAuthenticated, setIsAuthenticated] = useState(() => {
        // Check both sessionStorage and localStorage for the auth status
        return sessionStorage.getItem('isAuthenticated') === 'true' ||
            localStorage.getItem('isAuthenticated') === 'true';
    });

    useEffect(() => {
        // Sync the authentication status across sessionStorage and localStorage
        if (isAuthenticated) {
            sessionStorage.setItem('isAuthenticated', 'true');
            localStorage.setItem('isAuthenticated', 'true');
        } else {
            sessionStorage.removeItem('isAuthenticated');
            localStorage.removeItem('isAuthenticated');
        }
    }, [isAuthenticated]);

    const login = (persist = false) => {
        setIsAuthenticated(true);
        sessionStorage.setItem('isAuthenticated', 'true');
        if (persist) {
            localStorage.setItem('isAuthenticated', 'true');
        }
    };

    const logout = () => {
        setIsAuthenticated(false);
        sessionStorage.removeItem('isAuthenticated');
        localStorage.removeItem('isAuthenticated');
    };

    return (
        <AuthContext.Provider value={{ isAuthenticated, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
}

// Custom hook to use the AuthContext in other components
export function useAuth() {
    return useContext(AuthContext);
}
