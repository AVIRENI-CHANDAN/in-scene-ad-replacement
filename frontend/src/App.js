import '@fortawesome/fontawesome-free/css/all.min.css';
import React from 'react';
import { Route, Routes } from 'react-router-dom';
import './App.css';
import { AuthProvider } from './components/AuthContext';
import Dashboard from './components/Dashboard/Dashboard';
import LandingPage from './components/LandingPage/LandingPage';
import LoginPage from './components/LoginPage/LoginPage';
import NavigationBar from './components/NavigationBar/NavigationBar';
import NotFound from './components/NotFound/NotFound';
import NewProject from './components/Projects/NewProject/NewProject';
import Projects from './components/Projects/Projects';
import ProtectedRoute from './components/ProtectedRoute';
import RegistrationPage from './components/RegistrationPage/RegistrationPage';
import ScenePage from './components/ScenePage/ScenePage';

function App() {
  return (
    <AuthProvider>
      <div className="App" style={{ backgroundImage: `url(${process.env.PUBLIC_URL}/bg.jpeg)` }}>
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
              <Route path="/projects" element={<Projects />} />
              <Route path="/project/:project_id" element={<ScenePage />} />
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
