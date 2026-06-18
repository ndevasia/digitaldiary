import React, { useState, useEffect, useContext, useRef } from 'react';
import { ChevronLeft, Download } from 'lucide-react';
import VideoPlayer from '../components/VideoPlayer.jsx';
import { UserContext } from '../context/UserContext.jsx';
import { useMediaCache } from '../context/MediaCacheContext.jsx';

function FriendsPage() {
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';
  const currentUsername = useContext(UserContext).username || 'User';
  const apiBasePath = `${API_BASE_URL}/api/${encodeURIComponent(currentUsername)}`;
  const [friends, setFriends] = useState([]);
  const [friendsMediaData, setFriendsMediaData] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedFriend, setSelectedFriend] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [modalImage, setModalImage] = useState('');
  const mediaCache = useMediaCache();
  const pollingIntervalRef = useRef(null);

  useEffect(() => {
    fetchFriends();
    
    // Clean up polling interval on unmount
    return () => {
      if (pollingIntervalRef.current) {
        clearInterval(pollingIntervalRef.current);
      }
    };
  }, []);

  // Handle visibility changes - pause/resume polling
  useEffect(() => {
    const handleVisibilityChange = () => {
      if (document.visibilityState === 'hidden') {
        // Pause polling when tab is hidden
        if (pollingIntervalRef.current) {
          clearInterval(pollingIntervalRef.current);
          pollingIntervalRef.current = null;
        }
      } else {
        // Resume polling when tab becomes visible
        startPolling();
      }
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);
    return () => document.removeEventListener('visibilitychange', handleVisibilityChange);
  }, [friends]);

  // Listen for cache invalidation events
  useEffect(() => {
    const handleCacheInvalidation = () => {
      // When cache is invalidated, clear friend media cache and refetch
      refetchFriendsMedia();
    };

    window.addEventListener('mediaCache:invalidate', handleCacheInvalidation);
    return () => window.removeEventListener('mediaCache:invalidate', handleCacheInvalidation);
  }, [friends]);

  const refetchFriendsMedia = async () => {
    // Fetch media for all friends
    const friendsList = friends || [];
    if (friendsList.length === 0) return;

    const mediaPromises = friendsList.map(friendUsername =>
      fetchFriendMediaWithCache(friendUsername)
    );
    
    const resultsArray = await Promise.all(mediaPromises);
    const mediaData = {};
    resultsArray.forEach(({ friendUsername, media }) => {
      mediaData[friendUsername] = media;
    });
    
    setFriendsMediaData(mediaData);
  };

  const fetchFriendMediaWithCache = async (friendUsername) => {
    try {
      // Check cache first
      let media = mediaCache.get(friendUsername);
      
      if (!media) {
        // Cache miss, fetch from API
        const response = await fetch(`${API_BASE_URL}/api/${encodeURIComponent(friendUsername)}/media_aws`);
        if (response.ok) {
          media = await response.json();
          // Cache the data
          mediaCache.set(friendUsername, media);
        } else {
          media = [];
        }
      }
      
      return ({ friendUsername, media });
    } catch (err) {
      console.error(`Error fetching media for ${friendUsername}:`, err);
      return { friendUsername, media: [] };
    }
  };

  const startPolling = () => {
    // Clear any existing polling interval
    if (pollingIntervalRef.current) {
      clearInterval(pollingIntervalRef.current);
    }

    // Start polling every 90 seconds (1.5 minutes, within the 2-min cache TTL)
    pollingIntervalRef.current = setInterval(() => {
      if (document.visibilityState === 'visible') {
        refetchFriendsMedia();
      }
    }, 90000);
  };

  const fetchFriends = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${apiBasePath}/friends`);
      if (!response.ok) {
        throw new Error('Failed to fetch friends');
      }
      const data = await response.json();
      setFriends(data.friends || []);
      
      // Fetch media for all friends in parallel using cache
      const friendsList = data.friends || [];
      const mediaPromises = friendsList.map(friendUsername =>
        fetchFriendMediaWithCache(friendUsername)
      );
      
      const resultsArray = await Promise.all(mediaPromises);
      const mediaData = {};
      resultsArray.forEach(({ friendUsername, media }) => {
        mediaData[friendUsername] = media;
      });
      
      setFriendsMediaData(mediaData);
      setLoading(false);
      
      // Start polling for friend media updates
      startPolling();
    } catch (error) {
      console.error('Error fetching friends:', error);
      setError(error.message);
      setLoading(false);
    }
  };

  const handleFriendClick = (friendUsername) => {
    setSelectedFriend(friendUsername);
  };

  const handleBackClick = () => {
    setSelectedFriend(null);
  };

  const enlargeImage = (imageUrl) => {
    setModalImage(imageUrl);
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
  };

  const getScreenshotFileName = (item, fallbackPrefix = 'screenshot') => {
    const appName = (item.app_name || fallbackPrefix)
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-|-$/g, '');
    const dateStamp = item.timestamp
      ? new Date(item.timestamp).toISOString().split('T')[0]
      : 'unknown-date';
    return `${appName || fallbackPrefix}-${dateStamp}.png`;
  };

  const handleDownloadScreenshot = async (item, fallbackPrefix) => {
    try {
      const response = await fetch(item.media_url);
      if (!response.ok) {
        throw new Error('Unable to download screenshot');
      }
      const blob = await response.blob();
      const objectUrl = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = objectUrl;
      link.download = getScreenshotFileName(item, fallbackPrefix);
      document.body.appendChild(link);
      link.click();
      link.remove();
      URL.revokeObjectURL(objectUrl);
    } catch (error) {
      console.error('Failed to download screenshot:', error);
      window.open(item.media_url, '_blank', 'noopener,noreferrer');
    }
  };

  // Render the friends list
  const renderFriendsList = () => {
    if (friends.length === 0) {
      return (
        <div className="text-center py-12">
          <p className="text-gray-500">No friends added yet. Add friends in Settings!</p>
        </div>
      );
    }

    return (
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {friends.map(friendUsername => {
          const friendMedia = friendsMediaData[friendUsername] || [];
          
          // Find the most recent media item
          const sortedMedia = [...friendMedia].sort((a, b) => 
            new Date(b.timestamp) - new Date(a.timestamp)
          );
          const latestMedia = sortedMedia[0];
          
          // Get a representative image (screenshot)
          const screenshotMedia = friendMedia.find(item => item.type === 'screenshot');
          
          // Format the timestamp
          const lastActivityDate = latestMedia ? new Date(latestMedia.timestamp) : null;
          const lastActivity = lastActivityDate ? lastActivityDate.toLocaleDateString('en-US', {
            year: 'numeric', 
            month: 'short', 
            day: 'numeric'
          }) : 'No activity';
          
          return (
            <div 
              key={friendUsername} 
              className="bg-purple-100 rounded overflow-hidden shadow-sm transition-all hover:shadow-md hover:-translate-y-1 cursor-pointer group"
              onClick={() => handleFriendClick(friendUsername)}
            >
              <div className="h-40 overflow-hidden bg-purple-50 relative">
                {screenshotMedia ? (
                  <>
                    <img 
                      src={screenshotMedia.media_url} 
                      alt={friendUsername} 
                      className="w-full h-full object-cover"
                    />
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleDownloadScreenshot(screenshotMedia, friendUsername);
                      }}
                      className="absolute top-2 left-2 inline-flex items-center gap-1 px-2 py-1 text-xs bg-white/90 border border-gray-300 rounded hover:bg-white opacity-0 group-hover:opacity-100 transition-opacity"
                      title="Download screenshot"
                    >
                      <Download size={14} />
                    </button>
                  </>
                ) : (
                  <div className="w-full h-full flex items-center justify-center text-purple-500 font-semibold">
                    {friendUsername}
                  </div>
                )}
              </div>
              <div className="p-4">
                <h3 className="font-semibold text-gray-700 mb-1">{friendUsername}</h3>
                <div className="text-sm text-gray-600 mb-1">
                  {friendMedia.length} media item{friendMedia.length !== 1 ? 's' : ''}
                </div>
                <div className="text-xs text-gray-500">Last activity: {lastActivity}</div>
              </div>
            </div>
          );
        })}
      </div>
    );
  };

  // Render the friend detail view
  const renderFriendDetail = () => {
    if (!selectedFriend) return null;

    const friendMedia = friendsMediaData[selectedFriend] || [];
    
    // Sort media by timestamp (newest first)
    const sortedMedia = [...friendMedia].sort((a, b) => 
      new Date(b.timestamp) - new Date(a.timestamp)
    );

    if (sortedMedia.length === 0) {
      return (
        <div>
          <div className="mb-6">
            <button 
              onClick={handleBackClick}
              className="flex items-center text-teal-500 hover:text-teal-600 transition-colors"
            >
              <ChevronLeft size={20} className="mr-1" />
              Back to friends
            </button>
          </div>
          
          <h3 className="text-xl font-semibold text-gray-700 mb-4">{selectedFriend}'s Activity</h3>
          
          <div className="text-center py-12">
            <p className="text-gray-500">No media available for this friend.</p>
          </div>
        </div>
      );
    }

    return (
      <div>
        <div className="mb-6">
          <button 
            onClick={handleBackClick}
            className="flex items-center text-teal-500 hover:text-teal-600 transition-colors"
          >
            <ChevronLeft size={20} className="mr-1" />
            Back to friends
          </button>
        </div>
        
        <h3 className="text-xl font-semibold text-gray-700 mb-4">{selectedFriend}'s Activity</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {sortedMedia.map(item => {
            const date = new Date(item.timestamp).toLocaleDateString('en-US', {
              year: 'numeric', 
              month: 'short', 
              day: 'numeric'
            });
            
            let mediaClass = '';
            switch(item.type) {
              case 'video':
                mediaClass = 'bg-pink-200';
                break;
              case 'screenshot':
                mediaClass = 'bg-purple-100';
                break;
              case 'audio':
                mediaClass = 'bg-green-200';
                break;
              default:
                mediaClass = 'bg-purple-100';
            }
            
            if (item.type === 'screenshot') {
              return (
                <div 
                  key={item.media_id} 
                  className={`${mediaClass} rounded overflow-hidden shadow-sm relative group`}
                >
                  <div className="h-40 overflow-hidden bg-purple-50 cursor-pointer hover:opacity-80 transition-opacity"
                    onClick={() => enlargeImage(item.media_url)}>
                    <img 
                      src={item.media_url} 
                      alt="" 
                      className="w-full h-full object-cover"
                    />
                  </div>
                  <button
                    onClick={() => handleDownloadScreenshot(item, selectedFriend)}
                    className="absolute top-2 left-2 inline-flex items-center gap-1 px-2 py-1 text-xs bg-white/90 border border-gray-300 rounded hover:bg-white opacity-0 group-hover:opacity-100 transition-opacity"
                    title="Download screenshot"
                  >
                    <Download size={14} />
                  </button>
                  <div className="p-4">
                    <div className="text-sm text-gray-700 font-medium mb-1">Screenshot</div>
                    <div className="text-xs text-gray-500">{date}</div>
                  </div>
                </div>
              );
            } else if (item.type === 'video') {
              return (
                <div 
                  key={item.media_id} 
                  className={`${mediaClass} rounded overflow-hidden shadow-sm`}
                >
                  <div className="h-40 overflow-hidden bg-pink-50">
                    <VideoPlayer src={item.media_url} />
                  </div>
                  <div className="p-4">
                    <div className="text-sm text-gray-700 font-medium mb-1">Video</div>
                    <div className="text-xs text-gray-500">{date}</div>
                  </div>
                </div>
              );
            } else if (item.type === 'audio') {
              return (
                <div 
                  key={item.media_id} 
                  className={`${mediaClass} rounded overflow-hidden shadow-sm`}
                >
                  <div className="h-40 overflow-hidden bg-green-50 flex items-center justify-center">
                    <audio controls className="w-full">
                      <source src={item.media_url} type="audio/wav" />
                      Your browser does not support the audio element.
                    </audio>
                  </div>
                  <div className="p-4">
                    <div className="text-sm text-gray-700 font-medium mb-1">Audio</div>
                    <div className="text-xs text-gray-500">{date}</div>
                  </div>
                </div>
              );
            }
          })}
        </div>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="flex-1 p-8 overflow-y-auto">
        <header className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-semibold text-gray-700">Friends</h1>
        </header>
        <div className="text-center py-12">
          <p className="text-gray-500">Loading friends...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex-1 p-8 overflow-y-auto">
        <header className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-semibold text-gray-700">Friends</h1>
        </header>
        <div className="text-center py-12">
          <p className="text-red-500">Error: {error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 p-8 overflow-y-auto">
      <header className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-semibold text-gray-700">Friends</h1>
      </header>

      {showModal && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50"
          onClick={closeModal}
        >
          <img 
            src={modalImage} 
            alt="" 
            className="max-w-4xl max-h-screen object-contain"
            onClick={(e) => e.stopPropagation()}
          />
        </div>
      )}

      <div>
        {selectedFriend ? renderFriendDetail() : renderFriendsList()}
      </div>
    </div>
  );
}

export default FriendsPage;
