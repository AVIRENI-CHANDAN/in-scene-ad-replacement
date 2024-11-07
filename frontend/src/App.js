import React from 'react';
import './App.css';
import { AuthProvider } from './components/AuthContext';
import LandingPage from './components/LandingPage/LandingPage';
import NavigationBar from './components/NavigationBar/NavigationBar';

function App() {
  return (
    <AuthProvider>
      <div className='App'>
        <NavigationBar></NavigationBar>
        <LandingPage></LandingPage>
      </div>
    </AuthProvider>
  );
}

export default App;
