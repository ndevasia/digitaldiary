import React, { useState, useEffect } from 'react';
import { Mic, Video, Camera, X, Minus, Maximize, Minimize, BarChart2 } from 'lucide-react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
const { ipcRenderer } = window.require('electron');

const API_URL = 'http://localhost:5173/api';

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
      <Icon
        size={20}
      />
    </button>
    {tooltip && (
      <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 bg-black text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity">
        {tooltip}
      </div>
    )}
  </div>
);

function App() {
    const [isAudioRecording, setIsAudioRecording] = useState(false);
    const [isScreenRecording, setIsScreenRecording] = useState(false);
    const [isMaximized, setIsMaximized] = useState(false);

    // Add effect to listen for main window open/close events
    useEffect(() => {
        const handleMainWindowOpen = () => setIsMaximized(true);
        const handleMainWindowClose = () => setIsMaximized(false);

        ipcRenderer.on('main-window-opened', handleMainWindowOpen);
        ipcRenderer.on('main-window-closed', handleMainWindowClose);

        return () => {
            ipcRenderer.removeListener('main-window-opened', handleMainWindowOpen);
            ipcRenderer.removeListener('main-window-closed', handleMainWindowClose);
        };
    }, []);

    const handleResizeMouseDown = (e) => {
        e.preventDefault();
        e.stopPropagation();
        ipcRenderer.send('start-resize');

        const stopResize = () => {
            ipcRenderer.send('stop-resize');
            window.removeEventListener('mouseup', stopResize);
        };

        window.addEventListener('mouseup', stopResize);
    };

    const handleScreenshot = async () => {
        try {
            const response = await fetch(`${API_URL}/screenshot`, {
                method: 'POST'
            });
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
                const response = await fetch(`${API_URL}/recording/start`, {
                    method: 'POST'
                });
                const data = await response.json();
                if (data.error) {
                    console.error('Recording error:', data.error);
                    return;
                }
                setIsScreenRecording(true);
                console.log('Recording started:', data.path);
            } else {
                const response = await fetch(`${API_URL}/recording/stop`, {
                    method: 'POST'
                });
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
                const response = await fetch(`${API_URL}/audio/start`, {
                    method: 'POST'
                });
                const data = await response.json();
                if (data.error) {
                    console.error('Audio recording error:', data.error);
                    return;
                }
                setIsAudioRecording(true);
                console.log('Audio recording started:', data.path);
            } else {
                const response = await fetch(`${API_URL}/audio/stop`, {
                    method: 'POST'
                });
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

    // Toggle main window function
    const toggleMainWindow = () => {
        if (isMaximized) {
            ipcRenderer.send('close-main-window');
            setIsMaximized(false);
        } else {
            ipcRenderer.send('open-main-window');
            setIsMaximized(true);
        }
    };

    // Open main window function
    const openMainWindow = () => {
        ipcRenderer.send('open-main-window');
    };

    return (
        <Router>
            <div className="h-screen w-screen flex flex-col min-w-0 min-h-0 overflow-hidden bg-transparent">
                {/* Sidebar */}
                <div
                    className="bg-white flex flex-col min-w-0 min-h-0 p-1 rounded-lg border border-zinc-200 shadow-lg h-full relative"
                    style={{ WebkitAppRegion: 'drag' }}
                >
                    <div className="flex flex-col min-w-0 min-h-0 w-full h-full p-1 gap-2 items-center justify-between">
                        {/* Title bar */}
                        <div className="flex flex-row w-full justify-center gap-1 pb-2 border-b border-zinc-100" style={{ WebkitAppRegion: 'no-drag' }}>
                            <button
                                className="cursor-pointer aspect-square transition-all duration-200 p-0.5 rounded-full text-amber-950 bg-amber-400 hover:bg-amber-500"
                                onClick={() => ipcRenderer.send('minimize-window')}
                            >
                                <Minus size={14} />
                            </button>
                            <button
                                className="cursor-pointer aspect-square transition-all duration-200 p-0.5 rounded-full text-red-950 bg-red-400 hover:bg-red-500"
                                onClick={() => ipcRenderer.send('close-window')}
                            >
                                <X size={14} />
                            </button>
                        </div>

                        {/* Main toolbar */}
                        <div className="flex flex-col min-w-0 min-h-0 items-center gap-2" style={{ WebkitAppRegion: 'no-drag' }}>
                            <IconButton
                                icon={Camera}
                                onClick={handleScreenshot}
                                // tooltip="Take Screenshot"
                            />
                            <IconButton
                                icon={Video}
                                onClick={handleScreenRecording}
                                isActive={isScreenRecording}
                                // tooltip="Record Screen"
                            />
                            <IconButton
                                icon={Mic}
                                onClick={handleAudioRecording}
                                isActive={isAudioRecording}
                                // tooltip="Record Audio"
                            />
                            <Link to="/">
                                <IconButton
                                    icon={BarChart2}
                                    // tooltip="View Statistics"
                                />
                            </Link>
                            <IconButton
                                icon={isMaximized ? Minimize : Maximize}
                                onClick={toggleMainWindow}
                                // tooltip={isMaximized ? "Close Main Window" : "Open Main Window"}
                            />
                        </div>
                    </div>

                    {/* Resize handle */}
                    <div
                        className="mt-auto w-full h-6 cursor-s-resize flex items-center justify-center hover:bg-zinc-100 rounded"
                        style={{ WebkitAppRegion: 'no-drag' }}
                        onMouseDown={handleResizeMouseDown}
                    >
                        <div className="w-8 h-1 bg-zinc-400 rounded-full" />
                    </div>
                </div>

                {/* Main content */}
                <div className="flex-1 overflow-auto">
                    <Routes>
                        <Route path="/" element={<div />} />
                    </Routes>
                </div>
            </div>
        </Router>
    );
}

export default App;