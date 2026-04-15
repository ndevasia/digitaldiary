import { useCallback } from 'react';
import { useMediaCache } from '../context/MediaCacheContext';

/**
 * Custom hook for cache invalidation
 * Emits custom events to notify other components of cache changes
 * Also invalidates backend cache
 */
export const useCacheInvalidation = () => {
    const mediaCache = useMediaCache();
    
    const invalidateCache = useCallback(async (username) => {
        if (!username) return;
        
        // Invalidate frontend cache immediately (optimistic)
        mediaCache.invalidate(username);
        
        // Emit custom event for other components to listen to
        const event = new CustomEvent('mediaCache:invalidate', {
            detail: { username }
        });
        window.dispatchEvent(event);
        
        // Call backend cache invalidation endpoint
        try {
            const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 
                                 import.meta.env.VITE_API_BASE_URL || '';
            const apiBasePath = `${API_BASE_URL}/api/${encodeURIComponent(username)}`;
            
            const response = await fetch(`${apiBasePath}/cache/invalidate`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            
            if (!response.ok) {
                console.warn(`Failed to invalidate backend cache for user ${username}`);
            }
        } catch (error) {
            console.error('Error invalidating backend cache:', error);
            // Don't throw - invalidation is best-effort
        }
    }, [mediaCache]);
    
    return { invalidateCache };
};

export default useCacheInvalidation;
