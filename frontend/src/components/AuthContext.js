// AuthContext.js
import React, { createContext, useContext, useEffect, useState } from 'react';

const AuthContext = createContext();

export function AuthProvider({ children }) {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [loading, setLoading] = useState(true);

    const login = () => {
        setIsAuthenticated(true);
    };


    const logout = async () => {
        setIsAuthenticated(false);
        await fetch('/auth/logout', { method: 'POST', credentials: 'include' });
    };

    useEffect(() => {
        const checkAuthStatus = async () => {
            try {
                const response = await fetch('/auth/verify_access_token', {
                    method: 'POST',
                    credentials: 'include',
                });
                setIsAuthenticated(response.ok);
                console.log("Auth status:", response.ok); // Log authentication status
            } catch (error) {
                console.error('Error checking authentication status:', error);
            } finally {
                setLoading(false); // Set loading to false after check
                console.log("Loading status:", loading); // Log loading status
            }
        };

        checkAuthStatus();
    }, []);

    return (
        <AuthContext.Provider value={{ isAuthenticated, loading, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    return useContext(AuthContext);
}
