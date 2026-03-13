import React, { useState, useRef, useEffect } from 'react';
import { Mic, Video, Camera, X, Minus, Maximize, Minimize, BarChart2 } from 'lucide-react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import FFMpeg from './FFMpeg';
const { ipcRenderer } = window.require('electron');

const INACTIVE = "inactive";
const ACTIVE = "active";
const LOADING = "loading";

const IconButton = ({ icon: Icon, onClick, isLoading, isActive, tooltip }) => (
  <div className="relative group">
    <button
      onClick={onClick}
      className={`aspect-square p-4 rounded-lg flex items-center justify-center transition-all duration-200 ${
        isLoading
          ? 'cursor-not-allowed bg-zinc-300'
          : isActive
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
    const [screenshotState, setScreenshotState] = useState(INACTIVE);
    const [audioRecordingState, setAudioRecordingState] = useState(INACTIVE);
    const [screenRecordingState, setScreenRecordingState] = useState(INACTIVE);
    const screenRecordingUID = useRef(null);
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
        }
    });
    
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
        setScreenshotState(LOADING);
        FFMpeg.takeScreenshot().then(async (screenshot) => {
            setScreenshotState(INACTIVE);
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
        }).catch((err) => {
            console.error('Screenshot error:', err);
            setScreenshotState(INACTIVE);
        });
    };

    const handleScreenRecording = () => {
        try {
            setScreenRecordingState(LOADING);
            if (screenRecordingState === INACTIVE) {
                fetch('/api/recording/start', { method: 'POST' }).then(async (response) => {
                    if (!response.ok) {
                        throw new Error('Failed to start recording on backend');
                    }
                    const data = await response.json();
                    screenRecordingUID.current = data.uid;
                    const streamDestination = data.url;
                    const withAudio = localStorage.getItem('recordAudioWithScreen') === "true";
                    const audioDeviceName = localStorage.getItem('audioDeviceName');
                    FFMpeg.startVideoStream(streamDestination, withAudio, audioDeviceName).then(() => {
                        console.log('Screen recording started');
                        setScreenRecordingState(ACTIVE);
                    }).catch((err) => {
                        console.error('Screen recording error:', err);
                        setScreenRecordingState(INACTIVE);
                    });
                }).catch((err) => {
                    console.error('Recording start error:', err);
                    setScreenRecordingState(INACTIVE);
                });
            } else if (screenRecordingState === ACTIVE) {
                fetch(`/api/recording/stop/${screenRecordingUID.current}`, { method: 'POST' }).then(() => {
                    console.log('Notified backend of recording stop');
                    FFMpeg.stopVideoStream(true).then(() => {
                        console.log('Screen recording stopped');
                        setScreenRecordingState(INACTIVE);
                    }).catch((err) => {
                        console.error('Screen recording error:', err);
                        setScreenRecordingState(INACTIVE);
                    });
                }).catch((err) => {
                    console.error('Screen recording error:', err);
                    setScreenRecordingState(INACTIVE);
                });
            }
        } catch (error) {
            console.error('Recording error:', error);
            setScreenRecordingState(INACTIVE);
        }
    };

    const handleAudioRecording = async () => {
        try {
            setAudioRecordingState(LOADING);
            if (audioRecordingState === INACTIVE) {
                const audioDeviceName = localStorage.getItem('audioDeviceName');
                console.log('Using audio device:', audioDeviceName);
                FFMpeg.startAudioRecording(audioDeviceName).then(() => {
                    console.log('Audio recording started');
                    setAudioRecordingState(ACTIVE);
                }).catch((err) => {
                    console.error('Audio recording error:', err);
                    setAudioRecordingState(INACTIVE);
                });
            } else if (audioRecordingState === ACTIVE) {
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
                        } else {
                            console.error('Audio file upload failed');
                        }
                    }).catch((err) => {
                        console.error('Audio file upload error:', err);
                    });
                    setAudioRecordingState(INACTIVE);
                }).catch((err) => {
                    console.error('Audio recording error:', err);
                    setAudioRecordingState(INACTIVE);
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
                                isLoading={screenshotState == LOADING}
                                // tooltip="Take Screenshot"
                            />
                            <IconButton
                                icon={Video}
                                onClick={handleScreenRecording}
                                isLoading={screenRecordingState == LOADING}
                                isActive={screenRecordingState == ACTIVE}
                                // tooltip="Record Screen"
                            />
                            <IconButton
                                icon={Mic}
                                onClick={handleAudioRecording}
                                isLoading={audioRecordingState == LOADING}
                                isActive={audioRecordingState == ACTIVE}
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