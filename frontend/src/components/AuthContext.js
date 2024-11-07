// AuthContext.js
import React, { createContext, useContext, useState } from 'react';

// Create a Context for the authentication state
const AuthContext = createContext();

// AuthProvider component to wrap around the parts of the app that need access to auth state
export function AuthProvider({ children }) {
    const [isAuthenticated, setIsAuthenticated] = useState(() => {
        return localStorage.getItem('isAuthenticated') === 'true';
    });

    const login = () => {
        setIsAuthenticated(true);
        localStorage.setItem('isAuthenticated', 'true');
    };

    const logout = () => {
        setIsAuthenticated(false);
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
