// AuthContext.js
import React, { createContext, useContext, useEffect, useState } from 'react';

const AuthContext = createContext();

export function AuthProvider({ children }) {
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    const login = () => setIsAuthenticated(true);

    const logout = async () => {
        await fetch('/auth/logout', { method: 'POST', credentials: 'include' });
        setIsAuthenticated(false);
    };

    useEffect(() => {
        const checkAuthStatus = async () => {
            try {
                const response = await fetch('/auth/verify_access_token', {
                    method: 'POST',
                    credentials: 'include',
                });
                setIsAuthenticated(response.ok);
            } catch (error) {
                console.error('Error checking authentication status:', error);
            }
        };

        checkAuthStatus();
    }, []);

    return (
        <AuthContext.Provider value={{ isAuthenticated, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    return useContext(AuthContext);
}
