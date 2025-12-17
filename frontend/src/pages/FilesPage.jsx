import React, { useState, useEffect } from 'react';
import { ChevronDown } from 'lucide-react';
import Sidebar from '../components/Sidebar';

function FilesPage() {
    const [mediaList, setMediaList] = useState([]);
    const [filteredMedia, setFilteredMedia] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [filter, setFilter] = useState('all');
    const [userFilter, setUserFilter] = useState('all');
    const [showDropdown, setShowDropdown] = useState(false);
    const [users, setUsers] = useState([]);
    const [showAddUserModal, setShowAddUserModal] = useState(false);
    const [newUsername, setNewUsername] = useState('');
    const [addUserLoading, setAddUserLoading] = useState(false);
    const [addUserError, setAddUserError] = useState(null);

    useEffect(() => {
        fetchUsers();
        // initial media load will be handled by users/userFilter effect
    }, []);

    // Recompute filtered media whenever filter, userFilter, or mediaList changes
    useEffect(() => {
        let filtered = mediaList;

        // Apply media type filter
        if (filter !== 'all') {
            filtered = filtered.filter(item => item.type === filter);
        }

        // Apply user filter as a safeguard (mediaList may already be scoped by fetch)
        if (userFilter !== 'all') {
            filtered = filtered.filter(
                item => String(item.owner_user_id) === String(userFilter)
            );
        }

        setFilteredMedia(filtered);
    }, [filter, userFilter, mediaList]);

    useEffect(() => {
        fetchUsers();
        fetchMedia();
    }, []);

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
            const response = await fetch('/api/media_aws');
            if (!response.ok) {
                throw new Error('Failed to fetch media');
            }
            const data = await response.json();
            setMediaList(data);
            setFilteredMedia(data);
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
                    <div className="mb-8 flex justify-between items-center">
                        {/* User Filter Tabs */}
                        <div className="flex flex-wrap gap-2">
                            {users.map((user) => (
                                <button
                                    key={user.user_id}
                                    onClick={() => setUserFilter(user.user_id)}
                                    className={`px-4 py-2 rounded-full text-sm font-medium transition-colors duration-200 ${
                                        userFilter === user.user_id
                                            ? 'bg-teal-500 text-white'
                                            : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                                    }`}
                                >
                                    {user.username}
                                </button>
                            ))}
                            <button
                                onClick={() => {
                                    setNewUsername('');
                                    setAddUserError(null);
                                    setShowAddUserModal(true);
                                }}
                                className="px-4 py-2 rounded-full text-sm font-medium transition-colors duration-200 bg-gray-100 text-gray-600 hover:bg-gray-200"
                            >
                                Add User
                            </button>
                        </div>

                        {/* Media Filter Dropdown */}
                        <div className="relative">
                            <button
                                className="bg-teal-500 text-white px-4 py-2 rounded flex items-center"
                                onClick={() => setShowDropdown(!showDropdown)}
                            >
                                {getFilterDisplayName(filter)} <ChevronDown size={18} className="ml-2" />
                            </button>

                            {showDropdown && (
                                <div className="absolute top-full right-0 mt-1 bg-white shadow-md rounded-lg border border-gray-200 w-40 z-10">
                                    <ul>
                                        <li className="px-4 py-2 hover:bg-gray-100 text-teal-500 cursor-pointer" onClick={() => handleFilterChange('all')}>
                                            All
                                        </li>
                                        <li className="px-4 py-2 hover:bg-gray-100 text-teal-500 cursor-pointer" onClick={() => handleFilterChange('screenshot')}>
                                            Screenshots
                                        </li>
                                        <li className="px-4 py-2 hover:bg-gray-100 text-teal-500 cursor-pointer" onClick={() => handleFilterChange('audio')}>
                                            Audio
                                        </li>
                                        <li className="px-4 py-2 hover:bg-gray-100 text-teal-500 cursor-pointer" onClick={() => handleFilterChange('video')}>
                                            Video
                                        </li>
                                    </ul>
                                </div>
                            )}
                        </div>
                    </div>

                    {loading ? (
                        <div className="grid grid-cols-3 gap-6">
                            {[1, 2, 3, 4, 5, 6].map((_, index) => (
                                <div key={index} className="animate-pulse bg-blue-100 h-48 rounded"></div>
                            ))}
                        </div>
                    ) : error ? (
                        <div className="text-center py-12">
                            <p className="text-red-500">{error}</p>
                            <button
                                className="mt-4 bg-teal-500 text-white px-4 py-2 rounded hover:bg-teal-600"
                                onClick={fetchMedia}
                            >
                                Try Again
                            </button>
                        </div>
                    ) : filteredMedia.length === 0 ? (
                        <div className="text-center py-12">
                            <p className="text-gray-500">No media files found.</p>
                        </div>
                    ) : (
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                            {filteredMedia.map((item) => (
                                <div
                                    key={item.media_id}
                                    className="bg-white rounded-lg shadow-sm overflow-hidden p-4 flex flex-col"
                                >
                                    <div className="flex-grow">
                                        {renderMediaItem(item)}
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
            {/* Add User Modal */}
            {showAddUserModal && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
                    <div className="bg-white rounded-lg max-w-md w-full p-6">
                        <div className="flex justify-between items-center mb-4">
                            <h3 className="text-lg font-semibold">Add User</h3>
                            <button onClick={() => setShowAddUserModal(false)} className="text-gray-500 hover:text-gray-700">✕</button>
                        </div>

                        <div className="mb-4">
                            <label className="block text-sm text-gray-700 mb-2">Username</label>
                            <input
                                type="text"
                                className="w-full border border-gray-200 rounded px-3 py-2"
                                value={newUsername}
                                onChange={(e) => setNewUsername(e.target.value)}
                                placeholder="Enter username to add"
                            />
                            {addUserError && <p className="text-red-500 text-sm mt-2">{addUserError}</p>}
                        </div>

                        <div className="flex justify-end gap-2">
                            <button
                                className="px-4 py-2 rounded bg-gray-200 text-gray-700"
                                onClick={() => setShowAddUserModal(false)}
                            >
                                Cancel
                            </button>
                            <button
                                className="px-4 py-2 rounded bg-teal-500 text-white disabled:opacity-50"
                                onClick={async () => {
                                    const usernameToCheck = newUsername.trim();
                                    if (!usernameToCheck) {
                                        setAddUserError('Please enter a username');
                                        return;
                                    }

                                    try {
                                        setAddUserLoading(true);
                                        setAddUserError(null);

                                        // 1) Check S3 for the username
                                        const resp = await fetch(`/api/users_aws/check?username=${encodeURIComponent(usernameToCheck)}`);
                                        if (!resp.ok) {
                                            const err = await resp.json();
                                            throw new Error(err.error || 'Error checking username');
                                        }
                                        const data = await resp.json();
                                        if (!data.exists) {
                                            setAddUserError('User not found in S3');
                                            return;
                                        }

                                        // 2) Persist the username to user.json on the backend
                                        const addResp = await fetch('/api/users', {
                                            method: 'POST',
                                            headers: { 'Content-Type': 'application/json' },
                                            body: JSON.stringify({ username: usernameToCheck })
                                        });

                                        if (!addResp.ok) {
                                            const err = await addResp.json();
                                            throw new Error(err.error || 'Failed to add user');
                                        }

                                        if (addResp.status === 200) {
                                            // Already exists: fetch canonical user object from server so we have the integer id
                                            const usersResp = await fetch('/api/users');
                                            if (usersResp.ok) {
                                                const allUsers = await usersResp.json();
                                                const found = allUsers.find(u => u.username === usernameToCheck);
                                                if (found) {
                                                    setUsers(prev => {
                                                        const exists = prev.some(u => String(u.user_id) === String(found.user_id));
                                                        if (exists) return prev;
                                                        return [...prev, found];
                                                    });
                                                }
                                            }
                                        } else if (addResp.status === 201) {
                                            const newUser = await addResp.json();
                                            setUsers(prev => {
                                                const exists = prev.some(u => String(u.user_id) === String(newUser.user_id));
                                                if (exists) return prev;
                                                return [...prev, newUser];
                                            });
                                        }

                                        setShowAddUserModal(false);
                                        setNewUsername('');
                                    } catch (err) {
                                        console.error('Error adding user:', err);
                                        setAddUserError(err.message || 'Error adding user');
                                    } finally {
                                        setAddUserLoading(false);
                                    }
                                }}
                            >
                                {addUserLoading ? 'Checking...' : 'Add'}
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default FilesPage;