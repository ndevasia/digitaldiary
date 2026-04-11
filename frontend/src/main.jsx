import { useState, useEffect, StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { HashRouter as Router, Routes, Route } from 'react-router-dom';
import './index.css';
import App from './App.jsx';
import HomePage from './pages/HomePage.jsx';
import FilesPage from './pages/FilesPage.jsx';
import GamesPage from './pages/GamesPage';
import FriendsPage from './pages/FriendsPage.jsx';
import StatsPage from './pages/StatsPage';
import SettingsPage from './pages/SettingsPage.jsx';
import ScrapbookPage from './pages/ScrapbookPage.jsx';
import ScrapbookEditorPage from './pages/ScrapbookEditorPage.jsx';
import Sidebar from './components/Sidebar.jsx';
import { UserContext } from './context/UserContext.jsx';

const AUTH_USERNAME = import.meta.env.VITE_USERNAME;
const AUTH_SECRET = import.meta.env.VITE_USER_SECRET;
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:5001';

if (typeof window !== 'undefined' && !window.__digitalDiaryFetchAuthPatched) {
  const originalFetch = window.fetch.bind(window);
  const isFileProtocol = window.location.protocol === 'file:';

  window.fetch = (input, init = {}) => {
    const rawUrl = typeof input === 'string' ? input : input?.url;

    try {
      const resolvedUrl = new URL(rawUrl, window.location.origin);
      if (resolvedUrl.pathname.startsWith('/api/')) {
        const headers = new Headers(init.headers);
        headers.set('X-Username', AUTH_USERNAME || '');
        headers.set('X-User-Secret', AUTH_SECRET || '');

        // Vite proxy only exists in dev server. In packaged Electron (file://),
        // route API calls directly to the configured backend origin.
        const requestUrl = isFileProtocol
          ? `${API_BASE_URL}${resolvedUrl.pathname}${resolvedUrl.search}`
          : input;

        return originalFetch(requestUrl, { ...init, headers });
      }
    } catch (_) {
      // Fall through to original fetch if URL parsing fails.
    }

    return originalFetch(input, init);
  };

  window.__digitalDiaryFetchAuthPatched = true;
}

// Create a component to handle different render modes
function MainApp() {
  // Check if we should render the overlay tool or the full app
  const isOverlay = new URLSearchParams(window.location.search).has('overlay');
  const [currentUsername, setCurrentUsername] = useState(import.meta.env.VITE_USERNAME);

  useEffect(() => {
    if (currentUsername) {
      localStorage.setItem('username', currentUsername);
    }
    localStorage.setItem('userSecret', AUTH_SECRET || '');
  }, [currentUsername]);

  if (isOverlay) {
    return (
      <UserContext.Provider value={{ username: currentUsername }}>
        <App />
      </UserContext.Provider>
    );
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
            <Route path="/scrapbook" element={<ScrapbookPage />} />
            <Route path="/scrapbook/:scrapbookId" element={<ScrapbookEditorPage />} />
            <Route path="/friends" element={<FriendsPage />} />
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