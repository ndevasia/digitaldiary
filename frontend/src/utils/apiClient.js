/**
 * API client utility that automatically adds required headers including page source tracking
 */

import { useLocation } from 'react-router-dom';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001';

/**
 * Generate or retrieve the current session ID
 * SessionID persists for the entire app lifetime (from app open to app quit)
 */
export function getSessionId() {
  // Check if session ID already exists in sessionStorage (persists for this tab/window lifespan)
  let sessionId = sessionStorage.getItem('digitaldiary.sessionId');
  
  if (!sessionId) {
    // Generate new session ID: timestamp + random string
    const timestamp = new Date().toISOString().replace(/[:\-]/g, '').slice(0, 15); // YYYYMMDDTHHmmss
    const randomStr = Math.random().toString(36).substring(2, 10);
    sessionId = `${timestamp}-${randomStr}`;
    sessionStorage.setItem('digitaldiary.sessionId', sessionId);
  }
  
  return sessionId;
}

/**
 * Get the current page name based on the URL (supports HashRouter)
 */
export function getPageName() {
  // Get hash-based route (HashRouter uses #/path)
  const hash = window.location.hash;
  const pathname = window.location.pathname;
  
  // Check hash first (HashRouter uses this)
  if (hash.includes('scrapbook-editor')) return 'ScrapbookEditorPage';
  if (hash.includes('files')) return 'FilesPage';
  if (hash.includes('friends')) return 'FriendsPage';
  if (hash.includes('games')) return 'GamesPage';
  if (hash.includes('stats')) return 'StatsPage';
  if (hash.includes('settings')) return 'SettingsPage';
  if (hash.includes('scrapbook')) return 'ScrapbookPage';
  if (hash.includes('home') || hash === '#/') return 'HomePage';
  
  // Fallback to pathname-based detection
  if (pathname.includes('scrapbook-editor')) return 'ScrapbookEditorPage';
  if (pathname.includes('files')) return 'FilesPage';
  if (pathname.includes('friends')) return 'FriendsPage';
  if (pathname.includes('games')) return 'GamesPage';
  if (pathname.includes('home')) return 'HomePage';
  if (pathname.includes('stats')) return 'StatsPage';
  if (pathname.includes('scrapbook')) return 'ScrapbookPage';
  if (pathname.includes('settings')) return 'SettingsPage';
  
  // If no match, try to extract from hash path
  if (hash) {
    const routePath = hash.split('/')[1];
    if (routePath) {
      return routePath.charAt(0).toUpperCase() + routePath.slice(1);
    }
  }
  
  return 'HomePage'; // Default to HomePage instead of Unknown so header is always sent
}

/**
 * Wrapper around fetch that adds required headers for API calls
 * @param {string} url - The URL to fetch
 * @param {object} options - Fetch options
 * @returns {Promise} - Fetch response
 */
export async function apiFetch(url, options = {}) {
  // Get headers from options or create new object
  const headers = options.headers || {};
  
  // Add page source header
  const pageName = getPageName();
  headers['X-Page-Source'] = pageName;
  
  // Add session ID header
  const sessionId = getSessionId();
  headers['X-Session-ID'] = sessionId;
  
  // Return fetch with updated headers
  return fetch(url, {
    ...options,
    headers,
  });
}

/**
 * Build an API path for a specific endpoint
 * @param {string} username - The username
 * @param {string} endpoint - The endpoint (e.g., '/media_aws')
 * @returns {string} - Full API path
 */
export function buildApiPath(username, endpoint) {
  return `${API_BASE_URL}/api/${encodeURIComponent(username)}${endpoint}`;
}
