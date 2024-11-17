import React from 'react';
import { Route, Routes } from 'react-router-dom';
import './App.css';
import { AuthProvider } from './components/AuthContext';
import Dashboard from './components/Dashboard/Dashboard';
import NewProject from './components/Dashboard/NewProject/NewProject';
import LandingPage from './components/LandingPage/LandingPage';
import LoginPage from './components/LoginPage/LoginPage';
import NavigationBar from './components/NavigationBar/NavigationBar';
import NotFound from './components/NotFound/NotFound';
import ProtectedRoute from './components/ProtectedRoute';
import RegistrationPage from './components/RegistrationPage/RegistrationPage';

function App() {
  return (
    <AuthProvider>
      <div className="App">
        <NavigationBar />
        <div className="PageWrapper">
          <Routes>
            {/* Public Routes */}
            <Route path="/" element={<LandingPage />} />
            <Route path="/signup" element={<RegistrationPage />} />
            <Route path="/login" element={<LoginPage />} />

            {/* Protected Routes */}
            <Route element={<ProtectedRoute />}>
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/new/project" element={<NewProject />} />
              {/* Add other authenticated routes here */}
            </Route>

            {/* Fallback for unknown routes */}
            <Route path="*" element={<NotFound />} />
          </Routes>
        </div>
      </div>
    </AuthProvider>
  );
}

export default App;
