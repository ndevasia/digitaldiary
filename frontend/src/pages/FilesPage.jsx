import { useState, useEffect, useContext, useRef } from 'react';
import { ChevronDown, X, Loader, RefreshCw } from 'lucide-react';
import { UserContext } from '../context/UserContext.jsx';
import { useMediaCache } from '../context/MediaCacheContext.jsx';
import useCacheInvalidation from '../hooks/useCacheInvalidation.js';
import VideoPlayer from '../components/VideoPlayer.jsx';
import AudioPlayer from '../components/AudioPlayer.jsx';

function FilesPage() {
    const [mediaList, setMediaList] = useState([]);
    const [filteredMedia, setFilteredMedia] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [showDropdown, setShowDropdown] = useState(false);
    const [showGamesDropdown, setShowGamesDropdown] = useState(false);
    const [showModal, setShowModal] = useState(false);
    const [modalImage, setModalImage] = useState('');
    const [editingItemKey, setEditingItemKey] = useState(null);
    const [editingField, setEditingField] = useState(null);
    const [editValue, setEditValue] = useState('');
    const mediaDropdownRef = useRef(null);
    const gamesDropdownRef = useRef(null);
    const [games, setGames] = useState([]);
    const [filter, setFilter] = useState(new Set());
    const [gameFilter, setGameFilter] = useState(new Set());
    const [dateRange, setDateRange] = useState({ startDate: '', endDate: '' });
    const [dateRangeInfo, setDateRangeInfo] = useState({ min: '', max: '' });
    const [isRefreshing, setIsRefreshing] = useState(false);
    const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';
    const currentUsername = useContext(UserContext).username || 'User';
    const apiBasePath = `${API_BASE_URL}/api/${encodeURIComponent(currentUsername)}`;
    const abortControllerRef = useRef(null);
    
    // Initialize cache and invalidation utilities
    const mediaCache = useMediaCache();
    const { invalidateCache } = useCacheInvalidation();

    useEffect(() => {
        // Refetch data when page becomes visible (user navigates back)
        const handleVisibilityChange = () => {
            if (document.visibilityState === 'visible') {
                fetchMediaData();
            }
        };

        document.addEventListener('visibilitychange', handleVisibilityChange);
        return () => document.removeEventListener('visibilitychange', handleVisibilityChange);
    }, []);

    // Listen for cache invalidation events from other components
    useEffect(() => {
        const handleCacheInvalidation = (event) => {
            // Refetch media data when cache is invalidated
            fetchMediaData();
        };

        window.addEventListener('mediaCache:invalidate', handleCacheInvalidation);
        return () => window.removeEventListener('mediaCache:invalidate', handleCacheInvalidation);
    }, []);

    // Close dropdowns when clicking outside
    useEffect(() => {
        const handleDocumentClick = (e) => {
            const target = e.target;

            if (mediaDropdownRef.current && !mediaDropdownRef.current.contains(target)) {
                setShowDropdown(false);
            }
            if (gamesDropdownRef.current && !gamesDropdownRef.current.contains(target)) {
                setShowGamesDropdown(false);
            }
        };

        document.addEventListener('mousedown', handleDocumentClick);
        return () => document.removeEventListener('mousedown', handleDocumentClick);
    }, []);
    useEffect(() => {
        let filtered = mediaList;

        // Filter out items with invalid types or missing timestamps
        filtered = filtered.filter(item => 
            item.timestamp && ['video', 'audio', 'screenshot'].includes(item.type)
        );

        // Filter to only show current user's media
        filtered = filtered.filter(item => {
            const ownerUsername = item.s3_key.split('/')[0];
            return ownerUsername === currentUsername;
        });

        if (filter.size > 0) {
            filtered = filtered.filter(item => filter.has(item.type));
        }

        if (gameFilter.size > 0) {
            filtered = filtered.filter(item => gameFilter.has(item.app_name));
        }

        // apply date range filter
        if (dateRange.startDate || dateRange.endDate) {
            filtered = filtered.filter(item => {
                const itemDate = new Date(item.timestamp).toISOString().split('T')[0];
                if (dateRange.startDate && itemDate < dateRange.startDate) return false;
                if (dateRange.endDate && itemDate > dateRange.endDate) return false;
                return true;
            });
        }

        setFilteredMedia(filtered);
    }, [filter, gameFilter, mediaList, dateRange, currentUsername]);

    // calculate date range boundaries from media
    useEffect(() => {
        // Filter out invalid items before calculating date range
        const validMedia = mediaList.filter(item => 
            item.timestamp && ['video', 'audio', 'screenshot'].includes(item.type)
        );
        
        if (validMedia.length === 0) {
            setDateRangeInfo({ min: '', max: '' });
            return;
        }
        const dates = validMedia
            .map(item => new Date(item.timestamp).toISOString().split('T')[0])
            .sort();
        setDateRangeInfo({
            min: dates[0],
            max: dates[dates.length - 1]
        });
        if (!dateRange.startDate && !dateRange.endDate) {
            setDateRange({ startDate: dates[0], endDate: dates[dates.length - 1] });
        }
    }, [mediaList]);

    useEffect(() => {
        fetchMediaData();
        return () => {
            // Cancel any in-flight requests when dependencies change
            if (abortControllerRef.current) {
                abortControllerRef.current.abort();
            }
        };
    }, []);

    // auto-refresh media when the date range changes
    useEffect(() => {
        // only trigger a fetch if a date was actually picked
        if (dateRange.startDate || dateRange.endDate) {
            fetchMediaData();
        }
        return () => {
            if (abortControllerRef.current) {
                abortControllerRef.current.abort();
            }
        };
    }, [dateRange.startDate, dateRange.endDate]);


    const fetchMediaData = async () => {
        try {
            setLoading(true);
            setError(null);
            
            // Check cache first
            const cachedData = mediaCache.get(currentUsername);
            if (cachedData) {
                console.log('Using cached media data');
                setMediaList(cachedData);
                const uniqueGames = Array.from(
                    new Set(cachedData.map(item => item.app_name).filter(Boolean))
                );
                setGames(uniqueGames);
                setLoading(false);
                return;
            }
            
            // Fetch from API if cache miss
            const response = await fetch(`${apiBasePath}/media_aws`);
            if (!response.ok) {
                throw new Error('Failed to fetch media');
            }
            const data = await response.json();
            const sorted = data.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
            
            // Cache the data
            mediaCache.set(currentUsername, sorted);
            
            setMediaList(sorted);
            const uniqueGames = Array.from(
                new Set(sorted.map(item => item.app_name).filter(Boolean))
            );
            setGames(uniqueGames);
        } catch (error) {
            console.error('Error fetching media:', error);
            setError(error.message);
        } finally {
            setLoading(false);
        }
    };

    const handleManualRefresh = async () => {
        setIsRefreshing(true);
        try {
            // Clear local cache to force fresh fetch
            mediaCache.invalidate(currentUsername);
            // Invalidate backend cache as well
            await invalidateCache(currentUsername);
            // Force immediate fetch, bypassing cache
            await fetchMediaData();
        } catch (error) {
            console.error('Error during manual refresh:', error);
        } finally {
            setIsRefreshing(false);
        }
    };

    const handleFilterChange = (filterType) => {
        setFilter(filterType);
        setShowDropdown(false);
    };

    const getFilterDisplayName = (filterType) => {
        switch(filterType) {
            case 'all':
                return 'All';
            case 'screenshot':
                return 'Screenshots';
            case 'audio':
                return 'Audio';
            case 'video':
                return 'Video';
            default:
                return 'All';
        }
    };

    const handleDeleteMedia = async (item) => {
        if (!window.confirm(`Delete this ${item.type}?`)) return;

        try {
            // Use the s3_key directly from the item
            const s3Key = item.s3_key;
            if (!s3Key) {
                alert('Could not determine file location');
                console.error('No s3_key found in item:', item);
                return;
            }

            console.log('Deleting file with key:', s3Key);
            const response = await fetch(`${apiBasePath}/media/delete`, {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ file_key: s3Key })
            });

            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.error || `Server error: ${response.status}`);
            }

            const result = await response.json();
            console.log('Delete response:', result);

            // Remove using media_url as the unique identifier
            const updatedFiltered = filteredMedia.filter(m => m.media_url !== item.media_url);
            const updatedList = mediaList.filter(m => m.media_url !== item.media_url);

            setFilteredMedia(updatedFiltered);
            setMediaList(updatedList);
            
            // Invalidate cache for all pages
            await invalidateCache(currentUsername);
            
            alert('File deleted successfully');
        } catch (error) {
            console.error('Error deleting media:', error);
            alert('Error deleting file: ' + error.message);
        }
    };

    const enlargeImage = (imageUrl) => {
        setModalImage(imageUrl);
        setShowModal(true);
    };

    const closeModal = () => {
        setShowModal(false);
    };

    const startEditing = (s3Key, field, currentValue) => {
        setEditingItemKey(s3Key);
        setEditingField(field);
        setEditValue(currentValue || '');
    };

    const cancelEditing = () => {
        setEditingItemKey(null);
        setEditingField(null);
        setEditValue('');
    };

    const saveEditing = async (item) => {
        if (!editValue.trim()) {
            cancelEditing();
            return;
        }

        try {
            const trimmedValue = editValue.trim();
            const response = await fetch(`${apiBasePath}/media/update-metadata`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    s3_key: item.s3_key,
                    metadata: { [editingField]: trimmedValue }
                })
            });

            if (!response.ok) {
                throw new Error('Failed to update metadata');
            }

            // Update local media data
            const updatedList = mediaList.map(media => {
                if (media.s3_key === item.s3_key) {
                    return { ...media, [editingField]: trimmedValue };
                }
                return media;
            });
            setMediaList(updatedList);
            
            // Invalidate cache for all pages
            await invalidateCache(currentUsername);

            cancelEditing();
        } catch (error) {
            console.error('Error saving metadata:', error);
            alert('Error: ' + error.message);
        }
    };

    const renderEditableField = (label, value, item, field, isEditable = true) => {
        const isEditing = editingItemKey === item.s3_key && editingField === field;

        if (isEditing) {
            return (
                <div className="flex gap-2">
                    <input
                        type="text"
                        value={editValue}
                        onChange={(e) => setEditValue(e.target.value)}
                        onKeyDown={(e) => {
                            if (e.key === 'Enter') saveEditing(item);
                            if (e.key === 'Escape') cancelEditing();
                        }}
                        autoFocus
                        className="flex-1 px-2 py-1 border border-teal-500 rounded text-sm"
                    />
                    <button
                        onClick={() => saveEditing(item)}
                        className="px-2 py-1 bg-teal-500 text-white rounded text-xs hover:bg-teal-600"
                    >
                        Save
                    </button>
                    <button
                        onClick={cancelEditing}
                        className="px-2 py-1 bg-gray-300 text-gray-700 rounded text-xs hover:bg-gray-400"
                    >
                        Cancel
                    </button>
                </div>
            );
        }

        return (
            <div
                onDoubleClick={() => isEditable && startEditing(item.s3_key, field, value)}
                className={`px-2 py-1 rounded transition-colors ${
                    isEditable
                        ? 'cursor-pointer hover:bg-gray-100'
                        : 'cursor-not-allowed opacity-60'
                }`}
                title={isEditable ? 'Double-click to edit' : 'You do not have permission to edit this file'}
            >
                <span className="font-medium text-gray-700">{label}:</span> {value || 'Not set'}
            </div>
        );
    };

    const renderMediaItem = (item) => {
        // Format the timestamp
        const formatDate = (timestamp) => {
            if (!timestamp) return 'Jan 1, 2023'; // Default date if none available
            const date = new Date(timestamp);
            return date.toLocaleDateString('en-US', {
                month: 'short',
                day: 'numeric',
                year: 'numeric'
            });
        };

        // Determine background color based on media type
        let mediaClass = '';
        switch(item.type) {
            case 'video':
                mediaClass = 'bg-pink-200';
                break;
            case 'screenshot':
                mediaClass = 'bg-blue-100';
                break;
            case 'audio':
                mediaClass = 'bg-green-200';
                break;
            default:
                mediaClass = 'bg-blue-100';
        }

        // Extract owner username from s3_key (first part before /)
        const ownerUsername = item.s3_key.split('/')[0];
        const isOwned = ownerUsername === currentUsername;
        console.log(`File: ${item.s3_key}, ownerUsername: ${ownerUsername}, currentUsername: ${currentUsername}, isOwned: ${isOwned}`);

        switch (item.type) {
            case 'video':
                return (
                    <div className="h-full flex flex-col">
                        <div className={`${mediaClass} rounded overflow-hidden shadow-sm p-4 flex-grow flex justify-center items-center`}>
                            <VideoPlayer src={item.media_url} />
                        </div>
                        <div className="mt-2">
                            {renderEditableField('App', item.app_name, item, 'app_name', isOwned)}
                            <div className="text-xs text-gray-500 mt-1">{formatDate(item.timestamp)}</div>
                        </div>
                    </div>
                );
            case 'audio':
                return (
                    <div className="h-full flex flex-col">
                        <div className={`${mediaClass} rounded overflow-hidden shadow-sm p-4 flex-grow flex justify-center items-center`}>
                            <AudioPlayer src={item.media_url} />
                        </div>
                        <div className="mt-2">
                            {renderEditableField('App', item.app_name, item, 'app_name', isOwned)}
                            <div className="text-xs text-gray-500 mt-1">{formatDate(item.timestamp)}</div>
                        </div>
                    </div>
                );
            case 'screenshot':
                return (
                    <div className="h-full flex flex-col">
                        <div className={`${mediaClass} rounded overflow-hidden shadow-sm p-4 flex-grow flex justify-center items-center`}>
                            <img 
                                src={item.media_url} 
                                alt="Screenshot" 
                                className="w-full rounded cursor-pointer hover:opacity-90 transition-opacity"
                                onClick={() => enlargeImage(item.media_url)}
                            />
                        </div>
                        <div className="mt-2">
                            {renderEditableField('App', item.app_name, item, 'app_name', isOwned)}
                            <div className="text-xs text-gray-500 mt-1">{formatDate(item.timestamp)}</div>
                        </div>
                    </div>
                );
            default:
                return null;
        }
    };
    const renderImageModal = () => {
        if (!showModal) return null;

        return (
            <div
                className="fixed inset-0 bg-black bg-opacity-90 flex items-center justify-center z-50"
                onClick={closeModal}
            >
                <div
                    className="relative max-w-4xl max-h-[90vh]"
                    onClick={e => e.stopPropagation()}
                >
                    <button
                        className="absolute -top-10 -right-10 text-white text-3xl font-bold w-8 h-8 flex items-center justify-center"
                        onClick={closeModal}
                    >
                        &times;
                    </button>
                    <img
                        src={modalImage}
                        alt="Enlarged screenshot"
                        className="max-w-full max-h-[90vh] object-contain"
                    />
                </div>
            </div>
        );
    };
    return (
        <div className="h-screen flex flex-col">
            <div className="flex-1 p-8 overflow-y-auto">
                <header className="flex justify-between items-center mb-6">
                    <h1 className="text-2xl font-semibold text-gray-700">My Files</h1>
                    <button
                        onClick={handleManualRefresh}
                        disabled={isRefreshing}
                        className="p-2 rounded-full hover:bg-gray-100 transition-all disabled:opacity-50"
                        title="Refresh from AWS"
                    >
                        <RefreshCw 
                            size={24} 
                            className={`text-teal-600 ${isRefreshing ? 'animate-spin' : ''}`}
                        />
                    </button>
                </header>

                <div className="bg-white rounded-lg border border-gray-200 p-8">
                    <h2 className="text-xl font-medium text-gray-700 mb-4">Files</h2>

                    {/* Filters Section */}
                    <div className="mb-8">
                        {/* Media + App + Date Filters */}
                        <div className="flex flex-wrap gap-4">
                            {/* Media Type Dropdown */}
                            <div className="relative" ref={mediaDropdownRef}>
                            <button
                                className="bg-teal-500 text-white px-4 py-2 rounded flex justify-between items-center w-48"
                                onClick={() => setShowDropdown(!showDropdown)}
                            >
                                {filter.size === 0
                                ? 'All Types'
                                : Array.from(filter).map(f => getFilterDisplayName(f)).join(', ')}
                                <ChevronDown size={18} className="ml-2" />
                            </button>

                            {showDropdown && (
                                <div className="absolute top-full left-0 mt-1 bg-white shadow-md rounded-lg border border-gray-200 w-48 z-10">
                                <ul>
                                    {['screenshot', 'audio', 'video'].map(type => (
                                    <li
                                        key={type}
                                        className="px-4 py-2 hover:bg-gray-100 cursor-pointer flex items-center justify-between"
                                        onClick={() => {
                                        const newFilter = new Set(filter);
                                        if (newFilter.has(type)) newFilter.delete(type);
                                        else newFilter.add(type);
                                        setFilter(newFilter);
                                        }}
                                    >
                                        {getFilterDisplayName(type)}
                                        {filter.has(type) && <span>✔️</span>}
                                    </li>
                                    ))}
                                </ul>
                                </div>
                            )}
                            </div>
                            {/* Games Dropdown */}
                            <div className="relative" ref={gamesDropdownRef}>
                            <button
                                className="text-white px-4 py-2 rounded flex justify-between items-center w-48"
                                style={{ backgroundColor: '#44b785' }}
                                onClick={() => setShowGamesDropdown(!showGamesDropdown)}
                            >
                                {gameFilter.size === 0
                                ? 'All Apps'
                                : Array.from(gameFilter).join(', ')}
                                <ChevronDown size={18} className="ml-2" />
                            </button>

                            {showGamesDropdown && (
                                <div className="absolute top-full left-0 mt-1 bg-white shadow-md rounded-lg border border-gray-200 w-48 z-10">
                                <ul>
                                    {games
                                    .filter(g => g !== 'all') // remove the "all" placeholder
                                    .map(game => (
                                        <li
                                        key={game}
                                        className="px-4 py-2 hover:bg-gray-100 cursor-pointer flex items-center justify-between"
                                        onClick={() => {
                                            const newFilter = new Set(gameFilter);
                                            if (newFilter.has(game)) newFilter.delete(game);
                                            else newFilter.add(game);
                                            setGameFilter(newFilter);
                                        }}
                                        >
                                        {game}
                                        {gameFilter.has(game) && <span>✔️</span>}
                                        </li>
                                    ))}
                                </ul>
                                </div>
                            )}
                            </div>
                            {/* Date Range Filter */}
                            <div className="bg-gray-100 border border-gray-200 rounded px-4 py-2 flex gap-2 items-center"
                                style={{ backgroundColor: '#8ddab7' }}>
                                <input
                                    type="date"
                                    value={dateRange.startDate}
                                    onChange={(e) => setDateRange({ ...dateRange, startDate: e.target.value })}
                                    onBlur={() => {}}
                                    min={dateRangeInfo.min}
                                    max={dateRangeInfo.max}
                                    className="px-2 py-1 border border-gray-300 rounded text-sm text-gray-700 bg-white"
                                />
                                <span className="text-gray-600 text-sm">to</span>
                                <input
                                    type="date"
                                    value={dateRange.endDate}
                                    onChange={(e) => setDateRange({ ...dateRange, endDate: e.target.value })}
                                    onBlur={() => {}}
                                    min={dateRangeInfo.min}
                                    max={dateRangeInfo.max}
                                    className="px-2 py-1 border border-gray-300 rounded text-sm text-gray-700 bg-white"
                                />
                            </div>
                        </div>
                        {/* end Filters Section */}
                    </div>
                {/* Media Grid */}
                    <div className="w-full mt-6">
                        {loading ? (
                            <div className="flex flex-col items-center justify-center h-64 gap-4">
                                <Loader size={48} className="text-teal-500 animate-spin" />
                                <p className="text-gray-500 text-lg">Loading media...</p>
                            </div>
                        ) : error ? (
                            <div className="text-red-500">Error: {error}</div>
                        ) : filteredMedia.length === 0 ? (
                            <div className="text-gray-600">No media found.</div>
                        ) : (
                            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 mt-4">
                                {filteredMedia.map(item => {
                                    const ownerUsername = item.s3_key.split('/')[0];
                                    const isOwned = ownerUsername === currentUsername;
                                    return (
                                        <div key={item.s3_key} className="relative group bg-white rounded-lg border border-gray-100 p-4 h-64 flex flex-col">
                                            {renderMediaItem(item)}
                                            {!isOwned && (
                                                <div className="absolute top-2 left-2 bg-gray-400 text-white p-1 rounded" title="Read-only: owned by another user">
                                                    🔒
                                                </div>
                                            )}
                                            <button
                                                onClick={() => handleDeleteMedia(item)}
                                                disabled={!isOwned}
                                                className={`absolute top-2 right-2 p-1 rounded transition-opacity ${
                                                    isOwned
                                                        ? 'bg-red-500 hover:bg-red-600 text-white opacity-0 group-hover:opacity-100 cursor-pointer'
                                                        : 'bg-gray-300 text-gray-500 cursor-not-allowed opacity-50'
                                                }`}
                                                title={isOwned ? 'Delete this file' : 'You do not have permission to delete this file'}
                                            >
                                                <X size={16} />
                                            </button>
                                        </div>
                                    );
                                })}
                            </div>
                        )}
                    </div>
                </div>
            </div>
            {/* Image Modal */}
            {renderImageModal()}
        </div>
    );
}

export default FilesPage;