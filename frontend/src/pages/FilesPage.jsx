import React, { useState, useEffect, useRef } from 'react';
import { ChevronDown } from 'lucide-react';
import Sidebar from '../components/Sidebar';

function FilesPage() {
    const [mediaList, setMediaList] = useState([]);
    const [filteredMedia, setFilteredMedia] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [showDropdown, setShowDropdown] = useState(false);
    const [showUsersDropdown, setShowUsersDropdown] = useState(false);
    const [showGamesDropdown, setShowGamesDropdown] = useState(false);
    const mediaDropdownRef = useRef(null);
    const usersDropdownRef = useRef(null);
    const gamesDropdownRef = useRef(null);
    const [users, setUsers] = useState([]);
    const [games, setGames] = useState([]);
    const [filter, setFilter] = useState(new Set());
    const [userFilter, setUserFilter] = useState(new Set());
    const [gameFilter, setGameFilter] = useState(new Set());
    

    useEffect(() => {
        fetchUsers();
        fetchMedia();
    }, []);

    // Close dropdowns when clicking outside
    useEffect(() => {
        const handleDocumentClick = (e) => {
            const target = e.target;

            if (mediaDropdownRef.current && !mediaDropdownRef.current.contains(target)) {
                setShowDropdown(false);
            }
            if (usersDropdownRef.current && !usersDropdownRef.current.contains(target)) {
                setShowUsersDropdown(false);
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

        if (filter.size > 0) {
            filtered = filtered.filter(item => filter.has(item.type));
        }

        if (userFilter.size > 0) {
            filtered = filtered.filter(item => userFilter.has(item.owner_user_id.toString()));
        }

        if (gameFilter.size > 0) {
            filtered = filtered.filter(item => gameFilter.has(item.game));
        }

        setFilteredMedia(filtered);
    }, [filter, userFilter, gameFilter, mediaList]);


    const fetchUsers = async () => {
        try {
            const response = await fetch('/api/users');
            if (!response.ok) {
                throw new Error('Failed to fetch users');
            }
            const data = await response.json();
            // Only take the first two users plus 'all' option
            const limitedUsers = data.slice(0, 2);
            setUsers([{ user_id: 'all', username: 'All Users' }, ...limitedUsers]);
        } catch (error) {
            console.error('Error fetching users:', error);
            setError(error.message);
        }
    };

    const fetchMedia = async () => {
        try {
            setLoading(true);
            const response = await fetch('/api/media');
            if (!response.ok) {
                throw new Error('Failed to fetch media');
            }
            const data = await response.json();

            setMediaList(data);
            setFilteredMedia(data);

            // 🔹 Extract unique games
            const uniqueGames = Array.from(
                new Set(data.map(item => item.game).filter(Boolean))
            );

            setGames(['all', ...uniqueGames]);
        } catch (error) {
            console.error('Error fetching media:', error);
            setError(error.message);
        } finally {
            setLoading(false);
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

        switch (item.type) {
            case 'video':
                return (
                    <div className="h-full flex flex-col">
                        <div className={`${mediaClass} rounded overflow-hidden shadow-sm p-4 flex-grow flex justify-center items-center`}>
                            <video controls className="w-full rounded">
                                <source src={item.media_url} type="video/mp4" />
                                Your browser does not support the video tag.
                            </video>
                        </div>
                        <div className="mt-2">
                            <div className="font-medium text-gray-700">{item.game}</div>
                            <div className="text-xs text-gray-500">{formatDate(item.timestamp)}</div>
                        </div>
                    </div>
                );
            case 'audio':
                return (
                    <div className="h-full flex flex-col">
                        <div className={`${mediaClass} rounded overflow-hidden shadow-sm p-4 flex-grow flex justify-center items-center`}>
                            <audio controls className="w-full">
                                <source src={item.media_url} type="audio/mpeg" />
                                Your browser does not support the audio tag.
                            </audio>
                        </div>
                        <div className="mt-2">
                            <div className="font-medium text-gray-700">{item.game}</div>
                            <div className="text-xs text-gray-500">{formatDate(item.timestamp)}</div>
                        </div>
                    </div>
                );
            case 'screenshot':
                return (
                    <div className="h-full flex flex-col">
                        <div className={`${mediaClass} rounded overflow-hidden shadow-sm p-4 flex-grow flex justify-center items-center`}>
                            <img src={item.media_url} alt="Screenshot" className="w-full rounded" />
                        </div>
                        <div className="mt-2">
                            <div className="font-medium text-gray-700">{item.game}</div>
                            <div className="text-xs text-gray-500">{formatDate(item.timestamp)}</div>
                        </div>
                    </div>
                );
            default:
                return null;
        }
    };

    return (
        <div className="flex h-screen bg-blue-50">
            <Sidebar />

            <div className="flex-1 p-8 overflow-y-auto">
                <header className="flex justify-between items-center mb-6">
                    <h1 className="text-2xl font-semibold text-gray-700">Hello, User 1 & User 2</h1>
                </header>

                <div className="bg-white rounded-lg border border-gray-200 p-8">
                    <h2 className="text-xl font-medium text-gray-700 mb-4">Files</h2>

                {/* Filters Section */}
                    <div className="mb-8 flex flex-wrap gap-4">

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
                    {/* Users Dropdown */}
                    <div className="relative" ref={usersDropdownRef}>
                    <button
                        className="text-white px-4 py-2 rounded flex justify-between items-center w-48"
                        style={{ backgroundColor: '#3e8fa6' }}
                        onClick={() => setShowUsersDropdown(!showUsersDropdown)}
                    >
                        {userFilter.size === 0
                        ? 'All Users'
                        : Array.from(userFilter)
                            .map(id => users.find(u => u.user_id === parseInt(id))?.username || '')
                            .join(', ')}
                        <ChevronDown size={18} className="ml-2" />
                    </button>

                    {showUsersDropdown && (
                        <div className="absolute top-full left-0 mt-1 bg-white shadow-md rounded-lg border border-gray-200 w-48 z-10">
                        <ul>
                            {users
                            .filter(u => u.user_id !== 'all')
                            .map(user => (
                                <li
                                key={user.user_id}
                                className="px-4 py-2 hover:bg-gray-100 cursor-pointer flex items-center justify-between"
                                onClick={() => {
                                    const newFilter = new Set(userFilter);
                                    const idStr = user.user_id.toString();
                                    if (newFilter.has(idStr)) newFilter.delete(idStr);
                                    else newFilter.add(idStr);
                                    setUserFilter(newFilter);
                                }}
                                >
                                {user.username}
                                {userFilter.has(user.user_id.toString()) && <span>✔️</span>}
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
                    {/* end Filters Section */}
                    </div>
                {/* Media Grid */}
                    <div className="w-full mt-6">
                        {loading ? (
                            <div className="text-gray-500">Loading media...</div>
                        ) : error ? (
                            <div className="text-red-500">Error: {error}</div>
                        ) : filteredMedia.length === 0 ? (
                            <div className="text-gray-600">No media found.</div>
                        ) : (
                            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 mt-4">
                                {filteredMedia.map(item => (
                                    <div key={item.id || item.media_id || item.media_url} className="bg-white rounded-lg border border-gray-100 p-4 h-64 flex flex-col">
                                        {renderMediaItem(item)}
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default FilesPage;