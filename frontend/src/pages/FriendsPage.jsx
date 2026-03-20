import React, { useState, useEffect } from 'react';
import { ChevronLeft } from 'lucide-react';
import VideoPlayer from '../components/VideoPlayer.jsx';

function FriendsPage() {
  const [friends, setFriends] = useState([]);
  const [friendsMediaData, setFriendsMediaData] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedFriend, setSelectedFriend] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [modalImage, setModalImage] = useState('');

  useEffect(() => {
    fetchFriends();
  }, []);

  const fetchFriends = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/friends');
      if (!response.ok) {
        throw new Error('Failed to fetch friends');
      }
      const data = await response.json();
      setFriends(data.friends || []);
      
      // Fetch media for all friends in parallel using Promise.all
      const friendsList = data.friends || [];
      const mediaPromises = friendsList.map(friendUsername =>
        fetch(`/api/media_aws?username=${encodeURIComponent(friendUsername)}`)
          .then(response => {
            if (response.ok) {
              return response.json().then(mediaArray => ({
                friendUsername,
                media: mediaArray
              }));
            }
            return { friendUsername, media: [] };
          })
          .catch(err => {
            console.error(`Error fetching media for ${friendUsername}:`, err);
            return { friendUsername, media: [] };
          })
      );
      
      const resultsArray = await Promise.all(mediaPromises);
      const mediaData = {};
      resultsArray.forEach(({ friendUsername, media }) => {
        mediaData[friendUsername] = media;
      });
      
      setFriendsMediaData(mediaData);
      setLoading(false);
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
              className="bg-purple-100 rounded overflow-hidden shadow-sm transition-all hover:shadow-md hover:-translate-y-1 cursor-pointer"
              onClick={() => handleFriendClick(friendUsername)}
            >
              <div className="h-40 overflow-hidden bg-purple-50">
                {screenshotMedia ? (
                  <img 
                    src={screenshotMedia.media_url} 
                    alt={friendUsername} 
                    className="w-full h-full object-cover"
                  />
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
                  className={`${mediaClass} rounded overflow-hidden shadow-sm`}
                >
                  <div className="h-40 overflow-hidden bg-purple-50 cursor-pointer hover:opacity-80 transition-opacity"
                    onClick={() => enlargeImage(item.media_url)}>
                    <img 
                      src={item.media_url} 
                      alt="" 
                      className="w-full h-full object-cover"
                    />
                  </div>
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
                    <VideoPlayer url={item.media_url} />
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
