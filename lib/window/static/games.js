// games.js - Encapsulated to avoid conflicts with index.js
(function() {
    // Use a different variable name to avoid conflict with index.js
    let gamesMediaData = [];
  
    // Add a different event listener to avoid duplicating the same one in index.js
    window.addEventListener("load", initGamesPage);
  
    function initGamesPage() {
      fetchGamesData();
    }
  
    async function fetchGamesData() {
      try {
        let response = await fetch('/api/media');
        await gamesStatusCheck(response);
        gamesMediaData = await response.json();
        
        // Extract unique games and display them
        const uniqueGames = extractUniqueGames(gamesMediaData);
        displayGamesList(uniqueGames);
      } catch (error) {
        console.error('Error fetching games data:', error);
        displayGamesError(error.message);
      }
    }
  
    async function gamesStatusCheck(res) {
      if (!res.ok) {
        throw new Error(await res.text());
      }
      return res;
    }
  
    // Extract unique games from media items
    function extractUniqueGames(mediaItems) {
      // Create a map to store unique games
      const gamesMap = new Map();
      
      // Process each media item
      mediaItems.forEach(item => {
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
    }
  
    // Display the list of games
    function displayGamesList(games) {
      const gamesContainer = document.getElementById('games-container');
      
      if (!games || games.length === 0) {
        gamesContainer.innerHTML = `
          <div class="no-games">
            <p>No games available at the moment.</p>
          </div>
        `;
        return;
      }
      
      let gamesHTML = '<div class="games-grid">';
      
      games.forEach(game => {
        // Find the most recent media item for this game
        const sortedMedia = game.media.sort((a, b) => 
          new Date(b.timestamp) - new Date(a.timestamp)
        );
        const latestMedia = sortedMedia[0];
        
        // Get a representative image if available
        // Improved image selection logic
        const screenshotMedia = game.media.find(item => item.type === 'screenshot');
        const imageUrl = screenshotMedia ? 
                 screenshotMedia.media_url : 
                 `https://placehold.co/300x200/gray/white?text=${encodeURIComponent(game.name)}`;
       
        // Format the timestamp
        const lastPlayedDate = new Date(latestMedia.timestamp);
        const lastPlayed = lastPlayedDate.toLocaleDateString('en-US', {
          year: 'numeric', 
          month: 'short', 
          day: 'numeric'
        });
        
        gamesHTML += `
          <div class="game-card" onclick="window.showGameDetail('${game.slug}')">
            <div class="game-image">
              <img src="${imageUrl}" alt="${game.name}">
            </div>
            <div class="game-info">
              <h3>${game.name}</h3>
              <div class="media-count">${game.media.length} media item${game.media.length !== 1 ? 's' : ''}</div>
              <div class="last-played">Last played: ${lastPlayed}</div>
            </div>
          </div>
        `;
      });
      
      gamesHTML += '</div>';
      
      gamesContainer.innerHTML = gamesHTML;
      document.getElementById('games-container').style.display = 'block';
      document.getElementById('game-detail').style.display = 'none';
    }
  
    // Expose necessary functions to the window object for HTML onclick handlers
    window.showGameDetail = function(gameSlug) {
      // Find all media for this game
      const gameMedia = gamesMediaData.filter(item => 
        item.game && item.game.replace(/\s+/g, '-').toLowerCase() === gameSlug
      );
      
      if (gameMedia.length === 0) {
        console.error('No media found for game:', gameSlug);
        return;
      }
      
      // Get the game name from the first item
      const gameName = gameMedia[0].game;
      
      // Update the title
      document.getElementById('selected-game-title').textContent = gameName;
      
      // Sort media by timestamp (newest first)
      const sortedMedia = gameMedia.sort((a, b) => 
        new Date(b.timestamp) - new Date(a.timestamp)
      );
      
      // Generate HTML for the media items
      let mediaHTML = '';
      
      sortedMedia.forEach(item => {
        const date = new Date(item.timestamp).toLocaleDateString('en-US', {
          year: 'numeric', 
          month: 'short', 
          day: 'numeric'
        });
        
        // Different display based on media type
        if (item.type === 'screenshot') {
          mediaHTML += `
            <div class="media-item">
              <div class="media-thumbnail">
                <img src="${item.media_url}" alt="Screenshot">
              </div>
              <div class="media-info">
                <div class="media-type">Screenshot</div>
                <div class="media-date">${date}</div>
              </div>
            </div>
          `;
        } else if (item.type === 'video') {
          mediaHTML += `
            <div class="media-item">
              <div class="media-thumbnail video-thumbnail">
                <video src="${item.media_url}" controls></video>
              </div>
              <div class="media-info">
                <div class="media-type">Video</div>
                <div class="media-date">${date}</div>
              </div>
            </div>
          `;
        } else if (item.type === 'audio') {
          mediaHTML += `
            <div class="media-item">
              <div class="media-thumbnail audio-thumbnail">
                <audio src="${item.media_url}" controls></audio>
              </div>
              <div class="media-info">
                <div class="media-type">Audio</div>
                <div class="media-date">${date}</div>
              </div>
            </div>
          `;
        }
      });
      
      // Update the media container
      document.getElementById('game-media-container').innerHTML = mediaHTML;
      
      // Switch views
      document.getElementById('games-container').style.display = 'none';
      document.getElementById('game-detail').style.display = 'block';
    };
  
    // Return to the games list
    window.showGamesList = function() {
      document.getElementById('games-container').style.display = 'block';
      document.getElementById('game-detail').style.display = 'none';
    };
  
    // Display error message
    function displayGamesError(message) {
      const gamesContainer = document.getElementById('games-container');
      gamesContainer.innerHTML = `
        <div class="error-message">
          <p>Error loading games: ${message}</p>
        </div>
      `;
    }
  })();