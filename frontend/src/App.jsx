import React, { useState, useEffect, useRef } from 'react';
import { Mic, Video, Camera, X, Minus, Maximize, Minimize, BarChart2 } from 'lucide-react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import FFMpeg from './FFMpeg';
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
    const [isDragging, setIsDragging] = useState(false);
    const [isMaximized, setIsMaximized] = useState(false);
    const dragStartPos = useRef(null);

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
        // Effect to make sure an audio device is selected
        const audioDeviceName = localStorage.getItem('audioDeviceName');
        if (!audioDeviceName) {
            FFMpeg.getDevices().then(devices => {
                const audioDevices = devices.filter(d => d.type === 'audio');
                if (audioDevices.length > 0) {
                    localStorage.setItem('audioDeviceName', audioDevices[0].name);
                } else {
                    console.error('No audio devices found');
                }
            });
        }
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
            const screenshot = await FFMpeg.takeScreenshot();
            const formData = new FormData();
            formData.append('enctype', 'multipart/form-data');
            formData.append('file', screenshot);

            await fetch('/api/screenshot', {
                method: 'POST',
                body: formData,
            }).then((response) => {
                if (response.ok) {
                    console.log('Screenshot uploaded successfully');
                }
            }).catch((err) => {
                console.error('Screenshot upload error:', err);
            });
        } catch (error) {
            console.error('Screenshot error:', error);
        }
    };

    const handleScreenRecording = async () => {
        try {
            if (!isScreenRecording) {
                fetch('/api/recording/start', { method: 'POST' }).then(async (response) => {
                    if (!response.ok) {
                        throw new Error('Failed to start recording on backend');
                    }
                    const withAudio = localStorage.getItem('recordAudioWithScreen') === "true";
                    const streamDestination = (await response.json()).url;
                    FFMpeg.startVideoStream(streamDestination, withAudio).then(() => {
                        console.log('Screen recording started');
                        setIsScreenRecording(true);
                    }).catch((err) => {
                        console.error('Screen recording error:', err);
                    });
                }).catch((err) => {
                    console.error('Recording start error:', err);
                });
            } else {
                fetch('/api/recording/stop', { method: 'POST' }).then(() => {
                    console.log('Notified backend of recording stop');
                    FFMpeg.stopVideoStream().then(() => {
                        console.log('Screen recording stopped');
                        setIsScreenRecording(false);
                    }).catch((err) => {
                        console.error('Screen recording error:', err);
                        setIsScreenRecording(false);
                    });
                }).catch((err) => {
                    fetch('/api/recording/stop', { method: 'POST' });
                    console.error('Screen recording error:', err);
                    setIsScreenRecording(false);
                });
            }
        } catch (error) {
            console.error('Recording error:', error);
        }
    };

    const handleAudioRecording = async () => {
        try {
            if (!isAudioRecording) {
                const audioDeviceName = localStorage.getItem('audioDeviceName');
                console.log('Using audio device:', audioDeviceName);
                FFMpeg.startAudioRecording(audioDeviceName).then(() => {
                    console.log('Audio recording started');
                    setIsAudioRecording(true);
                }).catch((err) => {
                    console.error('Audio recording error:', err);
                });
            } else {
                FFMpeg.stopAudioRecording().then((audio_file) => {
                    console.log('Audio recording stopped');
                    const formData = new FormData();
                    formData.append('enctype', 'multipart/form-data');
                    formData.append('file', audio_file);
                    fetch('/api/audio/upload', {
                        method: 'POST',
                        body: formData,
                    }).then((response) => {
                        if (response.ok) {
                            console.log('Audio file uploaded successfully');
                        }
                    }).catch((err) => {
                        console.error('Audio file upload error:', err);
                    });
                    setIsAudioRecording(false);
                }).catch((err) => {
                    console.error('Audio recording error:', err);
                    setIsAudioRecording(false);
                });
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
            <div className="flex h-screen">
                {/* Sidebar */}
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