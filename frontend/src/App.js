import React from 'react';
import { Route, Routes } from 'react-router-dom';
import './App.css';
import { AuthProvider } from './components/AuthContext';
import Dashboard from './components/Dashboard/Dashboard';
import LandingPage from './components/LandingPage/LandingPage';
import LoginPage from './components/LoginPage/LoginPage';
import NavigationBar from './components/NavigationBar/NavigationBar';
import NotFound from './components/NotFound/NotFound';
import RegistrationPage from './components/RegistrationPage/RegistrationPage';

function App() {
  return (
    <AuthProvider>
      <div className='App'>
        <NavigationBar></NavigationBar>
        <div className='PageWrapper'>
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/signup" element={<RegistrationPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </div>
      </div>
    </AuthProvider>
  );
}

export default App;
