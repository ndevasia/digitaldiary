import React, { createContext, useContext } from 'react';

const CacheContext = createContext();

// Cache TTL in milliseconds (2 minutes)
const CACHE_TTL = 2 * 60 * 1000;

/**
 * MediaCacheContext - Provides caching utilities for media data
 * Uses localStorage to store media lists with TTL
 */
export const MediaCacheProvider = ({ children }) => {
    const cache = {
        /**
         * Get cached media data for a username
         * @param {string} username - The username to get cache for
         * @returns {Array|null} - Cached media list or null if expired/not found
         */
        get: (username) => {
            try {
                const key = `media_cache_${username}`;
                const cached = localStorage.getItem(key);
                
                if (!cached) return null;
                
                const { data, timestamp } = JSON.parse(cached);
                const now = Date.now();
                
                // Check if cache has expired
                if (now - timestamp > CACHE_TTL) {
                    localStorage.removeItem(key);
                    return null;
                }
                
                return data;
            } catch (error) {
                console.error('Error reading from cache:', error);
                return null;
            }
        },
        
        /**
         * Set cached media data for a username
         * @param {string} username - The username to set cache for
         * @param {Array} data - The media data to cache
         */
        set: (username, data) => {
            try {
                const key = `media_cache_${username}`;
                const cacheData = {
                    data,
                    timestamp: Date.now()
                };
                localStorage.setItem(key, JSON.stringify(cacheData));
            } catch (error) {
                console.error('Error writing to cache:', error);
            }
        },
        
        /**
         * Clear cache for a username
         * @param {string} username - The username to clear cache for
         */
        invalidate: (username) => {
            try {
                const key = `media_cache_${username}`;
                localStorage.removeItem(key);
            } catch (error) {
                console.error('Error invalidating cache:', error);
            }
        },
        
        /**
         * Clear cache for a specific username (used when switching accounts)
         * @param {string} username - The username to clear
         */
        clear: (username) => {
            cache.invalidate(username);
        }
    };
    
    return (
        <CacheContext.Provider value={cache}>
            {children}
        </CacheContext.Provider>
    );
};

/**
 * Hook to use media cache
 * @returns {Object} - Cache object with get, set, invalidate, and clear methods
 */
export const useMediaCache = () => {
    const context = useContext(CacheContext);
    if (!context) {
        throw new Error('useMediaCache must be used within MediaCacheProvider');
    }
    return context;
};
