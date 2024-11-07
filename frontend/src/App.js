import React from 'react';
import { AuthProvider } from './components/AuthContext';
import NavigationBar from './components/NavigationBar/NavigationBar';

function App() {
  return (
    <AuthProvider>
      <NavigationBar></NavigationBar>
    </AuthProvider>
  );
}

export default App;
