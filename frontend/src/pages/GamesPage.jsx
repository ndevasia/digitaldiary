import React, { useState, useEffect, useContext } from 'react';
import { ChevronLeft } from 'lucide-react';
import { UserContext } from '../context/UserContext.jsx';
import VideoPlayer from '../components/VideoPlayer.jsx';

function GamesPage() {
  const [mediaData, setMediaData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedGame, setSelectedGame] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [modalImage, setModalImage] = useState('');
  const currentUsername = useContext(UserContext).username || 'User';

  useEffect(() => {
    fetchMediaData();
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
      if (item.game) {
        // Create a slug (URL-friendly ID) from the game name
        const gameSlug = item.game.replace(/\s+/g, '-').toLowerCase();
        
        // If this game isn't in our map yet, add it
        if (!gamesMap.has(gameSlug)) {
          gamesMap.set(gameSlug, {
            name: item.game,
            slug: gameSlug,
            media: []
          });
        }
        
        // Add this media to the game's media array
        gamesMap.get(gameSlug).media.push(item);
      }
    });
    
    // Convert map to array and sort by game name
    return Array.from(gamesMap.values()).sort((a, b) => 
      a.name.localeCompare(b.name)
    );
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
                  key={item.media_id} 
                  className={`${mediaClass} rounded overflow-hidden shadow-sm`}
                >
                  <div className="p-4">
                    <img 
                      src={item.media_url} 
                      alt="Screenshot" 
                      className="w-full rounded cursor-pointer hover:opacity-90 transition-opacity" 
                      onClick={() => enlargeImage(item.media_url)}
                    />
                    <div className="mt-2">
                      <div className="font-medium text-gray-700">{item.game}</div>
                      <div className="text-xs text-gray-500">{date}</div>
                    </div>
                  </div>
                </div>
              );
            } else if (item.type === 'video') {
              return (
                <div 
                  key={item.media_id} 
                  className={`${mediaClass} rounded overflow-hidden shadow-sm`}
                >
                  <div className="p-4">
                    <VideoPlayer src={item.media_url} />
                    <div className="mt-2">
                      <div className="font-medium text-gray-700">{item.game}</div>
                      <div className="text-xs text-gray-500">{date}</div>
                    </div>
                  </div>
                </div>
              );
            } else if (item.type === 'audio') {
              return (
                <div 
                  key={item.media_id} 
                  className={`${mediaClass} rounded overflow-hidden shadow-sm`}
                >
                  <div className="p-4">
                    <audio controls className="w-full mb-2">
                      <source src={item.media_url} type="audio/mpeg" />
                      Your browser does not support the audio tag.
                    </audio>
                    <div className="mt-2">
                      <div className="font-medium text-gray-700">{item.game}</div>
                      <div className="text-xs text-gray-500">{date}</div>
                    </div>
                  </div>
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
    <div>
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