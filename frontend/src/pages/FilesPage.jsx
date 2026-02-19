import { useState, useEffect, useContext, useRef } from 'react';
import { ChevronDown } from 'lucide-react';
import { UserContext } from '../context/UserContext.jsx';

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
    const [showAddUserModal, setShowAddUserModal] = useState(false);
    const [newUsername, setNewUsername] = useState('');
    const [addUserLoading, setAddUserLoading] = useState(false);
    const [addUserError, setAddUserError] = useState(null);
    const currentUsername = useContext(UserContext).username || 'User';
    const abortControllerRef = useRef(null);

    useEffect(() => {
        fetchUsers();
        // initial media load will be handled by users/userFilter effect
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

    // Recompute filtered media whenever filter, userFilter, or mediaList changes
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
        
        // Apply user filter as a safeguard (mediaList may already be scoped by fetch)
        if (userFilter !== 'all') {
            filtered = filtered.filter(
                item => String(item.owner_user_id) === String(userFilter)
            );
        }

        setFilteredMedia(filtered);
    }, [filter, userFilter, gameFilter, mediaList]);

    useEffect(() => {
        fetchMedia();
        return () => {
            // Cancel any in-flight requests when dependencies change
            if (abortControllerRef.current) {
                abortControllerRef.current.abort();
            }
        };
    }, [userFilter, users]);

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
          // Cancel any previous request
          if (abortControllerRef.current) {
              abortControllerRef.current.abort();
          }
          abortControllerRef.current = new AbortController();
          const signal = abortControllerRef.current.signal;

          setLoading(true);
          setError(null);

          // If "All Users" is selected, fetch per-user and concatenate results
          const isAllSelected = userFilter.size === 0 || userFilter.has('all');

        if (isAllSelected) {
            const userList = users
                .filter(u => String(u.user_id) !== 'all')
                .map(u => u.username);

            if (userList.length === 0) {
                const resp = await fetch(`/api/media_aws?username=${encodeURIComponent(currentUsername)}`, { signal });
                if (!resp.ok) throw new Error('Failed to fetch media');
                const data = await resp.json();
                setMediaList(data);
                const uniqueGames = Array.from(
                  new Set(data.map(item => item.game).filter(Boolean))
                );
                setGames(uniqueGames);
                setGameFilter(new Set()); // Clear game filter when switching users
                return;
            }

            const promises = userList.map(async (u) => {
                const resp = await fetch(`/api/media_aws?username=${encodeURIComponent(u)}`, { signal });
                return resp.ok ? resp.json() : [];
            });

            const arrays = await Promise.all(promises);
            const merged = arrays.flat();
            setMediaList(merged);
            const uniqueGames = Array.from(
              new Set(merged.map(item => item.game).filter(Boolean))
            );
            setGames(uniqueGames);
            setGameFilter(new Set()); // Clear game filter when switching users
            return;
        }

        // Single user selected; `userFilter` holds the username
        const usernames = users
            .filter(u => userFilter.has(String(u.user_id)))
            .map(u => u.username || u.user_id);
        const promises = usernames.map(async (username) => {
            const resp = await fetch(`/api/media_aws?username=${encodeURIComponent(username)}`, { signal });
            if (!resp.ok) return [];
            return resp.json();
        });
          
        const arrays = await Promise.all(promises);
        const data = arrays.flat();
        setMediaList(data);
        const uniqueGames = Array.from(
          new Set(data.map(item => item.game).filter(Boolean))
        );
        setGames(uniqueGames);
        setGameFilter(new Set()); // Clear game filter when switching users
      } catch (error) {
          if (error.name !== 'AbortError') {
              console.error('Error fetching media:', error);
              setError(error.message);
          }
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
        <div>
            <div className="flex-1 p-8 overflow-y-auto">
                <header className="flex justify-between items-center mb-6">
                    <h1 className="text-2xl font-semibold text-gray-700">Hello, {currentUsername}</h1>
                </header>

                <div className="bg-white rounded-lg border border-gray-200 p-8">
                    <h2 className="text-xl font-medium text-gray-700 mb-4">Files</h2>

                    {/* Filters Section */}
                    <div className="mb-8 flex justify-between items-start gap-6">
                        {/* User Filter Tabs */}
                        <div className="flex flex-wrap gap-2">
                            {users.map((user) => (
                                  <button
                                      onClick={() => {
                                        if (user.user_id === 'all') {
                                            setUserFilter(new Set()); // Clearing the set represents "All"
                                        } else {
                                            const newSet = new Set(userFilter);
                                            newSet.delete('all'); // Remove 'all' if a specific user is picked
                                            const id = String(user.user_id);
                                            if (newSet.has(id)) newSet.delete(id);
                                            else newSet.add(id);
                                            setUserFilter(newSet);
                                        }
                                    }}
                                      className={`px-4 py-2 rounded-full text-sm font-medium transition-colors duration-200 ${
                                          (user.user_id === 'all' && userFilter.size === 0) || userFilter.has(String(user.user_id))
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
                    {/* Media + App Filters */}
                    <div className="flex gap-4"></div>
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