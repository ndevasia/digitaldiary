import { useState, useEffect, StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './index.css';
import App from './App.jsx';
import HomePage from './pages/HomePage.jsx';
import FilesPage from './pages/FilesPage.jsx';
import GamesPage from './pages/GamesPage';
import StatsPage from './pages/StatsPage';
import SettingsPage from './pages/SettingsPage.jsx';
import Sidebar from './components/Sidebar.jsx';
import { UserContext } from './context/UserContext.jsx';

// Create a component to handle different render modes
function MainApp() {
  // Check if we should render the overlay tool or the full app
  const isOverlay = new URLSearchParams(window.location.search).has('overlay');
  const [currentUsername, setCurrentUsername] = useState('User');

  if (isOverlay) {
    return <App />;
  } else {
    useEffect(() => {
        const fetchCurrentUser = async () => {
            try {
                const res = await fetch('/api/current_user');
                if (!res.ok) return;
                const data = await res.json();
                if (data.username) setCurrentUsername(data.username);
            } catch (err) {
                console.error('Error fetching current user:', err);
            }
        };
        fetchCurrentUser();
    }, []);
  }

  return (
    <Router>
      <UserContext.Provider value={{ username: currentUsername }}>
        <div className="flex h-screen bg-blue-50">
          <Sidebar />
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/files" element={<FilesPage />} />
            <Route path="/games" element={<GamesPage />} />
            <Route path="/stats" element={<StatsPage />} />
            <Route path="/journals" element={<HomePage />} /> {/* Placeholder */}
            <Route path="/settings" element={<SettingsPage />} />
          </Routes>
        </div>
      </UserContext.Provider>
    </Router>
  );
}

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <MainApp />
  </StrictMode>
);