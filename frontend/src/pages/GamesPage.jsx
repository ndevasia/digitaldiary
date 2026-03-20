import React, { useState, useEffect, useContext } from 'react';
import { ChevronLeft, X } from 'lucide-react';
import { UserContext } from '../context/UserContext.jsx';
import VideoPlayer from '../components/VideoPlayer.jsx';
import AudioPlayer from '../components/AudioPlayer.jsx';

function GamesPage() {
  const [mediaData, setMediaData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedGame, setSelectedGame] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [modalImage, setModalImage] = useState('');
  const [editingItemKey, setEditingItemKey] = useState(null);
  const [editingField, setEditingField] = useState(null);
  const [editValue, setEditValue] = useState('');
  const currentUsername = useContext(UserContext).username || 'User';

  useEffect(() => {
    fetchMediaData();

    // Refetch data when page becomes visible (user navigates back)
    const handleVisibilityChange = () => {
      if (document.visibilityState === 'visible') {
        fetchMediaData();
      }
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);
    return () => document.removeEventListener('visibilitychange', handleVisibilityChange);
  }, []);

  const fetchMediaData = async () => {
    try {
      setLoading(true);
      const response = await fetch(`/api/media_aws?username=${encodeURIComponent(currentUsername)}`);
      if (!response.ok) {
        throw new Error('Failed to fetch media');
      }
      const data = await response.json();
      setMediaData(data);
      
      // Log all media with their app_names
      console.log('Raw media data from API:');
      data.forEach((item, index) => {
        console.log(`  [${index}] s3_key="${item.s3_key}" app_name="${item.app_name}"`);
      });
      
      setLoading(false);
    } catch (error) {
      console.error('Error fetching media data:', error);
      setError(error.message);
      setLoading(false);
    }
  };

  const extractUniqueGames = () => {
    // Create a map to store unique games
    const gamesMap = new Map();
    
    // Process each media item
    mediaData.forEach(item => {
      if (item.app_name) {
        // Create a slug (URL-friendly ID) from the app name
        const gameSlug = item.app_name.replace(/\s+/g, '-').toLowerCase();
        
        console.log(`Processing media: app_name="${item.app_name}" (slug="${gameSlug}")`);
        
        // If this app isn't in our map yet, add it
        if (!gamesMap.has(gameSlug)) {
          gamesMap.set(gameSlug, {
            name: item.app_name,
            slug: gameSlug,
            media: []
          });
        }
        
        // Add this media to the app's media array
        gamesMap.get(gameSlug).media.push(item);
      }
    });
    
    const games = Array.from(gamesMap.values()).sort((a, b) => 
      a.name.localeCompare(b.name)
    );
    
    console.log('Unique games found:', games.map(g => ({ name: g.name, count: g.media.length })));
    
    return games;
  };

  const handleGameClick = (game) => {
    setSelectedGame(game);
  };

  const handleBackClick = () => {
    setSelectedGame(null);
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
      const response = await fetch('/api/media/update-metadata', {
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
      const updatedData = mediaData.map(media => {
        if (media.s3_key === item.s3_key) {
          return { ...media, [editingField]: trimmedValue };
        }
        return media;
      });
      setMediaData(updatedData);

      // Update selectedGame if it's currently being viewed
      if (selectedGame) {
        const updatedGame = {
          ...selectedGame,
          media: selectedGame.media.map(m => 
            m.s3_key === item.s3_key ? { ...m, [editingField]: trimmedValue } : m
          )
        };
        setSelectedGame(updatedGame);
      }

      cancelEditing();
    } catch (error) {
      console.error('Error saving metadata:', error);
      alert('Error: ' + error.message);
    }
  };

  const renderEditableField = (label, value, item, field) => {
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
            className="flex-1 px-2 py-1 border border-teal-500 rounded"
          />
          <button
            onClick={() => saveEditing(item)}
            className="px-2 py-1 bg-teal-500 text-white rounded text-sm hover:bg-teal-600"
          >
            Save
          </button>
          <button
            onClick={cancelEditing}
            className="px-2 py-1 bg-gray-300 text-gray-700 rounded text-sm hover:bg-gray-400"
          >
            Cancel
          </button>
        </div>
      );
    }

    return (
      <div
        onDoubleClick={() => startEditing(item.s3_key, field, value)}
        className="cursor-pointer hover:bg-gray-100 px-2 py-1 rounded transition-colors"
        title="Double-click to edit"
      >
        <span className="font-medium">{label}:</span> {value || 'Not set'}
      </div>
    );
  };


  // Get unique games
  const games = extractUniqueGames();

  // Render the games list
  const renderGamesList = () => {
    if (games.length === 0) {
      return (
        <div className="text-center py-12">
          <p className="text-gray-500">No apps available at the moment.</p>
        </div>
      );
    }

    return (
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {games.map(game => {
          // Find the most recent media item for this game
          const sortedMedia = [...game.media].sort((a, b) => 
            new Date(b.timestamp) - new Date(a.timestamp)
          );
          const latestMedia = sortedMedia[0];
          
          // Get a representative image if available
          //This searches through all media associated with the game to find the first one with type 'screenshot'.
          const screenshotMedia = game.media.find(item => item.type === 'screenshot');
          
          // Format the timestamp
          const lastPlayedDate = new Date(latestMedia.timestamp);
          const lastPlayed = lastPlayedDate.toLocaleDateString('en-US', {
            year: 'numeric', 
            month: 'short', 
            day: 'numeric'
          });
          
          return (
            <div 
              key={game.slug} 
              className="bg-blue-100 rounded overflow-hidden shadow-sm transition-all hover:shadow-md hover:-translate-y-1 cursor-pointer"
              onClick={() => handleGameClick(game)}
            >
              <div className="h-40 overflow-hidden bg-blue-50">
                {screenshotMedia ? (
                  <img 
                    src={screenshotMedia.media_url} 
                    alt={game.name} 
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <div className="w-full h-full flex items-center justify-center text-blue-500 font-semibold">
                    {game.name}
                  </div>
                )}
              </div>
              <div className="p-4">
                <h3 className="font-semibold text-gray-700 mb-1">{game.name}</h3>
                <div className="text-sm text-gray-600 mb-1">
                  {game.media.length} media item{game.media.length !== 1 ? 's' : ''}
                </div>
                <div className="text-xs text-gray-500">Last memory: {lastPlayed}</div>
              </div>
            </div>
          );
        })}
      </div>
    );
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
      const response = await fetch('/api/media/delete', {
        method: 'POST',
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
      const updatedMedia = selectedGame.media.filter(m => m.media_url !== item.media_url);
      const updatedGame = { ...selectedGame, media: updatedMedia };
      setSelectedGame(updatedGame);

      // Also update full media data
      const updatedData = mediaData.filter(m => m.media_url !== item.media_url);
      setMediaData(updatedData);
      
      alert('File deleted successfully');
    } catch (error) {
      console.error('Error deleting media:', error);
      alert('Error deleting file: ' + error.message);
    }
  };

  // Render the game detail view
  const renderGameDetail = () => {
    if (!selectedGame) return null;

    // Sort media by timestamp (newest first)
    const sortedMedia = [...selectedGame.media].sort((a, b) => 
      new Date(b.timestamp) - new Date(a.timestamp)
    );

    return (
      <div>
        <div className="mb-6">
          <button 
            onClick={handleBackClick}
            className="flex items-center text-teal-500 hover:text-teal-600 transition-colors"
          >
            <ChevronLeft size={20} className="mr-1" />
            Back to apps
          </button>
        </div>
        
        <h3 className="text-xl font-semibold text-gray-700 mb-4">{selectedGame.name}</h3>
        
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
                mediaClass = 'bg-blue-100';
                break;
              case 'audio':
                mediaClass = 'bg-green-200';
                break;
              default:
                mediaClass = 'bg-blue-100';
            }
            
            if (item.type === 'screenshot') {
              return (
                <div 
                  key={item.s3_key} 
                  className={`${mediaClass} rounded overflow-hidden shadow-sm relative group`}
                >
                  <div className="p-4">
                    <img 
                      src={item.media_url} 
                      alt="Screenshot" 
                      className="w-full rounded cursor-pointer hover:opacity-90 transition-opacity" 
                      onClick={() => enlargeImage(item.media_url)}
                    />
                    <div className="mt-2">
                      {renderEditableField('App', item.app_name, item, 'app_name')}
                      <div className="text-xs text-gray-500 mt-1">{date}</div>
                    </div>
                  </div>
                  <button
                    onClick={() => handleDeleteMedia(item)}
                    className="absolute top-2 right-2 bg-red-500 hover:bg-red-600 text-white p-1 rounded opacity-0 group-hover:opacity-100 transition-opacity"
                    title="Delete this file"
                  >
                    <X size={16} />
                  </button>
                </div>
              );
            } else if (item.type === 'video') {
              return (
                <div 
                  key={item.s3_key} 
                  className={`${mediaClass} rounded overflow-hidden shadow-sm relative group`}
                >
                  <div className="p-4">
                    <VideoPlayer src={item.media_url} />
                    <div className="mt-2">
                      {renderEditableField('App', item.app_name, item, 'app_name')}
                      <div className="text-xs text-gray-500 mt-1">{date}</div>
                    </div>
                  </div>
                  <button
                    onClick={() => handleDeleteMedia(item)}
                    className="absolute top-2 right-2 bg-red-500 hover:bg-red-600 text-white p-1 rounded opacity-0 group-hover:opacity-100 transition-opacity"
                    title="Delete this file"
                  >
                    <X size={16} />
                  </button>
                </div>
              );
            } else if (item.type === 'audio') {
              return (
                <div 
                  key={item.s3_key} 
                  className={`${mediaClass} rounded overflow-hidden shadow-sm relative group`}
                >
                  <div className="p-4">
                    <AudioPlayer src={item.media_url} />
                    <div className="mt-2">
                      {renderEditableField('App', item.app_name, item, 'app_name')}
                      <div className="text-xs text-gray-500 mt-1">{date}</div>
                    </div>
                  </div>
                  <button
                    onClick={() => handleDeleteMedia(item)}
                    className="absolute top-2 right-2 bg-red-500 hover:bg-red-600 text-white p-1 rounded opacity-0 group-hover:opacity-100 transition-opacity"
                    title="Delete this file"
                  >
                    <X size={16} />
                  </button>
                </div>
              );
            }
            return null;
          })}
        </div>
      </div>
    );
  };

  // Image Modal/Lightbox
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
    <div className="flex flex-col h-full">
      <div className="flex-1 p-8 overflow-y-auto">
        <header className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-semibold text-gray-700">Hello, {currentUsername}</h1>
        </header>
        
        <section className="mb-8">
          <h2 className="text-xl font-medium text-gray-700 mb-4">Apps</h2>
          
          <div className="bg-white rounded-lg border border-gray-200 p-8">
            {loading ? (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {[1, 2, 3, 4, 5, 6].map((_, index) => (
                  <div key={index} className="animate-pulse bg-blue-100 h-48 rounded"></div>
                ))}
              </div>
            ) : error ? (
              <div className="text-center py-12">
                <p className="text-red-500">{error}</p>
                <button 
                  className="mt-4 bg-teal-500 text-white px-4 py-2 rounded hover:bg-teal-600"
                  onClick={fetchMediaData}
                >
                  Try Again
                </button>
              </div>
            ) : selectedGame ? (
              renderGameDetail()
            ) : (
              renderGamesList()
            )}
          </div>
        </section>
      </div>
      
      {renderImageModal()}
    </div>
  );
}

export default GamesPage;