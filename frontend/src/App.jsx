import React, { useState, useEffect, useRef } from 'react';
import { Mic, Video, Camera, X, Minus, Maximize, Minimize } from 'lucide-react';

const API_URL = 'http://localhost:5001/api';

const IconButton = ({ icon: Icon, onClick, isActive, tooltip }) => (
  <div className="relative group">
    <button
      onClick={onClick}
      className={`aspect-square p-4 rounded-lg flex items-center justify-center transition-all duration-200 ${
        isActive 
          ? 'bg-blue-500 text-zinc-50 ' 
          : 'bg-zinc-100 hover:bg-zinc-200 border border-zinc-200/50'
      }`}
    >
      <Icon size={20} />
    </button>
  </div>
);

function App() {
    const [isAudioRecording, setIsAudioRecording] = useState(false);
    const [isScreenRecording, setIsScreenRecording] = useState(false);
    const [isDragging, setIsDragging] = useState(false);
    const [isMaximized, setIsMaximized] = useState(false);
    const [gameId, setGameId] = useState(null);
    const dragStartPos = useRef(null);

    const ipc = window.electron?.ipcRenderer;

    // Fetch latest game ID when component mounts
    useEffect(() => {
        const fetchLatestSession = async () => {
            try {
                const response = await fetch(`${API_URL}/session/latest`);
                const data = await response.json();
                
                if (data.error) {
                    console.error('Session fetch error:', data.error);
                    return;
                }
                
                if (data && data.game_id) {
                    setGameId(data.game_id);
                    console.log('Latest game ID loaded:', data.game_id);
                } else {
                    console.log('No previous game ID found.');
                }
            } catch (error) {
                console.error('Session fetch error:', error);
            }
        };

        fetchLatestSession();
    }, []);

    // Listen for game ID updates
    useEffect(() => {
        const handleGameIdUpdated = (newGameId) => {
            setGameId(newGameId);
            console.log('Game ID updated to:', newGameId);
        };

        const handleUpdateGameIdRequest = (newGameId) => {
            console.log('Received update-game-id request:', newGameId);
            updateGameId(newGameId)
                .then(success => {
                    if (success && ipc) {
                        // Notify main process that the update was successful
                        ipc.send('game-id-updated-success', newGameId);
                    }
                });
        };

        ipc?.on('game-id-updated', handleGameIdUpdated);
        ipc?.on('update-game-id', handleUpdateGameIdRequest);

        return () => {
            ipc?.removeListener('game-id-updated', handleGameIdUpdated);
            ipc?.removeListener('update-game-id', handleUpdateGameIdRequest);
        };
    }, [ipc]);

    // Listen for main window open/close
    useEffect(() => {
        const handleMainWindowOpen = () => setIsMaximized(true);
        const handleMainWindowClose = () => setIsMaximized(false);

        ipc?.on('main-window-opened', handleMainWindowOpen);
        ipc?.on('main-window-closed', handleMainWindowClose);

        return () => {
            ipc?.removeListener('main-window-opened', handleMainWindowOpen);
            ipc?.removeListener('main-window-closed', handleMainWindowClose);
        };
    }, [ipc]);

    useEffect(() => {
        const handleMouseMove = (e) => {
            if (!isDragging || !dragStartPos.current) return;
            const deltaX = e.screenX - dragStartPos.current.x;
            const deltaY = e.screenY - dragStartPos.current.y;
            ipc?.send('dragging', { x: deltaX, y: deltaY });
            dragStartPos.current = { x: e.screenX, y: e.screenY };
        };

        const handleMouseUp = () => {
            setIsDragging(false);
            dragStartPos.current = null;
        };

        if (isDragging) {
            document.addEventListener('mousemove', handleMouseMove);
            document.addEventListener('mouseup', handleMouseUp);
        }

        return () => {
            document.removeEventListener('mousemove', handleMouseMove);
            document.removeEventListener('mouseup', handleMouseUp);
        };
    }, [isDragging, ipc]);

    const handleMouseDown = (e) => {
        setIsDragging(true);
        dragStartPos.current = { x: e.screenX, y: e.screenY };
    };

    const handleScreenshot = async () => {
        try {
            const response = await fetch(`${API_URL}/screenshot`, { method: 'POST' });
            const data = await response.json();

            if (data.error) {
                console.error('Screenshot error:', data.error);
                return;
            }
            console.log('Screenshot saved:', data.path);
        } catch (error) {
            console.error('Screenshot error:', error);
        }
    };

    const handleScreenRecording = async () => {
        try {
            if (!isScreenRecording) {
                const response = await fetch(`${API_URL}/recording/start`, { method: 'POST' });
                const data = await response.json();

                if (data.error) {
                    console.error('Recording error:', data.error);
                    return;
                }
                setIsScreenRecording(true);
                console.log('Recording started:', data.path);
            } else {
                const response = await fetch(`${API_URL}/recording/stop`, { method: 'POST' });
                const data = await response.json();

                if (data.error) {
                    console.error('Recording error:', data.error);
                    return;
                }
                setIsScreenRecording(false);
                console.log('Recording stopped:', data.video_path);
                console.log('Thumbnail created:', data.thumbnail_path);
            }
        } catch (error) {
            console.error('Recording error:', error);
        }
    };

    const handleAudioRecording = async () => {
        try {
            if (!isAudioRecording) {
                const response = await fetch(`${API_URL}/audio/start`, { method: 'POST' });
                const data = await response.json();

                if (data.error) {
                    console.error('Audio recording error:', data.error);
                    return;
                }
                setIsAudioRecording(true);
                console.log('Audio recording started:', data.path);

            } else {
                const response = await fetch(`${API_URL}/audio/stop`, { method: 'POST' });
                const data = await response.json();

                if (data.error) {
                    console.error('Audio recording error:', data.error);
                    return;
                }
                setIsAudioRecording(false);
                console.log('Audio recording stopped:', data.path);
            }
        } catch (error) {
            console.error('Audio recording error:', error);
        }
    };

    const toggleMainWindow = () => {
        if (isMaximized) {
            ipc?.send('close-main-window');
            setIsMaximized(false);
        } else {
            ipc?.send('open-main-window');
            setIsMaximized(true);
        }
    };

    const openMainWindow = () => {
        ipc?.send('open-main-window');
    };

    // Handle game ID input
    const handleGameIdInput = () => {
        ipc?.send('openInputWindow');
    };

    // Update game ID directly from App.jsx if needed
    const updateGameId = async (newGameId) => {
        try {
            const response = await fetch(`${API_URL}/session/update`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ game_id: newGameId })
            });
            const data = await response.json();
            
            if (data.error) {
                console.error('Game ID update error:', data.error);
                return false;
            }
            
            setGameId(newGameId);
            console.log('Game ID updated successfully:', newGameId);
            return true;
        } catch (error) {
            console.error('Game ID update error:', error);
            return false;
        }
    };

    return (
        <div
            className="border border-red-500 bg-white flex flex-col p-1 rounded-lg"
            onMouseDown={handleMouseDown}
        >
            <div className="flex flex-col w-full h-full p-1 gap-2 items-center justify-between">
                {/* Title bar */}
                <div className="flex flex-row w-full justify-center gap-1">
                    <button
                        className="cursor-pointer aspect-square transition-all duration-200 p-0.5 rounded-full text-amber-950 bg-amber-400 hover:bg-amber-500"
                        onClick={() => ipc?.send('minimize-window')}
                    >
                        <Minus size={14} />
                    </button>
                    <button
                        className="cursor-pointer aspect-square transition-all duration-200 p-0.5 rounded-full text-red-950 bg-red-400 hover:bg-red-500"
                        onClick={() => ipc?.send('close-window')}
                    >
                        <X size={14} />
                    </button>
                </div>

                {/* Main toolbar */}
                <div className="flex flex-col items-center gap-1">
                    <IconButton icon={Camera} onClick={handleScreenshot} />
                    <IconButton
                        icon={Video}
                        onClick={handleScreenRecording}
                        isActive={isScreenRecording}
                    />
                    <IconButton
                        icon={Mic}
                        onClick={handleAudioRecording}
                        isActive={isAudioRecording}
                    />
                    <IconButton
                        icon={isMaximized ? Minimize : Maximize}
                        onClick={toggleMainWindow}
                        tooltip={isMaximized ? "Close Main Window" : "Open Main Window"}
                    />
                    
                    {/* Game ID display and edit button */}
                    <div className="mt-2 text-center">
                        <div className="text-xs text-gray-500 mb-1">Game</div>
                        <button 
                            onClick={handleGameIdInput}
                            className="text-sm px-2 py-1 bg-gray-100 hover:bg-gray-200 rounded truncate max-w-[60px]"
                            title={gameId || "Set game ID"}
                        >
                            {gameId ? gameId.slice(0, 8) + (gameId.length > 8 ? '...' : '') : "None"}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default App;