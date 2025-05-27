import React, { useState, useEffect, useRef } from 'react';
import { Mic, Video, Camera, X, Minus, Maximize, Minimize } from 'lucide-react';
import { HashRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './auth/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Login from './pages/Login';
import './auth/aws-config';
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
  </div>
);

function MainApp() {
    const [isAudioRecording, setIsAudioRecording] = useState(false);
    const [isScreenRecording, setIsScreenRecording] = useState(false);
    const [isDragging, setIsDragging] = useState(false);
    const [isMaximized, setIsMaximized] = useState(false);
    const dragStartPos = useRef(null);
    const { signOut } = useAuth();

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

    useEffect(() => {
        const handleMouseMove = (e) => {
            if (!isDragging || !dragStartPos.current) return;
            const deltaX = e.screenX - dragStartPos.current.x;
            const deltaY = e.screenY - dragStartPos.current.y;
            ipcRenderer.send('dragging', { x: deltaX, y: deltaY });
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
    }, [isDragging]);

    const handleMouseDown = (e) => {
        setIsDragging(true);
        dragStartPos.current = { x: e.screenX, y: e.screenY };
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
        <div 
            className="border border-red-500 bg-white flex flex-col p-1 rounded-lg" 
            onMouseDown={handleMouseDown}
        >
            <div className="flex flex-col w-full h-full p-1 gap-2 items-center justify-between">
                {/* Title bar */}
                <div className="flex flex-row w-full justify-center gap-1">
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
                <div className="flex flex-col items-center gap-1">
                    <IconButton 
                        icon={Camera} 
                        onClick={handleScreenshot}
                    />
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
                </div>
            </div>
        </div>
    );
}

function App() {
    return (
        <AuthProvider>
            <Router>
                <Routes>
                    <Route path="/login" element={<Login />} />
                    <Route
                        path="/"
                        element={
                            <ProtectedRoute>
                                <MainApp />
                            </ProtectedRoute>
                        }
                    />
                    <Route path="*" element={<Navigate to="/" replace />} />
                </Routes>
            </Router>
        </AuthProvider>
    );
}

export default App;