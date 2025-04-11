import React from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './index.css';
import App from './App.jsx';
import HomePage from './pages/HomePage.jsx';
import FilesPage from './pages/FilesPage.jsx';
import GamesPage from './pages/GamesPage';


// Create a component to handle different render modes
function MainApp() {
  // Check if we should render the overlay tool or the full app
  const isOverlay = new URLSearchParams(window.location.search).has('overlay');
  
  if (isOverlay) {
    return <App />;
  }
  
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/files" element={<FilesPage />} />
        <Route path="/games" element={<GamesPage />} /> {/* Placeholder */}
        <Route path="/journals" element={<HomePage />} /> {/* Placeholder */}
        <Route path="/settings" element={<HomePage />} /> {/* Placeholder */}
      </Routes>
    </Router>
  );
}

createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <MainApp />
  </React.StrictMode>
);