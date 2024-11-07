import React from 'react';
import { Route, Routes } from 'react-router-dom';
import './App.css';
import { AuthProvider } from './components/AuthContext';
import LandingPage from './components/LandingPage/LandingPage';
import NavigationBar from './components/NavigationBar/NavigationBar';

function App() {
  return (
    <AuthProvider>
      <div className='App'>
        <NavigationBar></NavigationBar>
        <div className='PageWrapper'>
          <Routes>
            <Route path="/" element={<LandingPage />} />
          </Routes>
        </div>
      </div>
    </AuthProvider>
  );
}

export default App;
