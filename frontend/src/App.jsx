import React, { useState, useEffect, useRef } from 'react';
import { Mic, Video, Camera, X, Minus } from 'lucide-react';
const { ipcRenderer } = window.require('electron');

const API_URL = 'http://localhost:5000/api';

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
    {/* {tooltip && (
      <div className="absolute left-12 top-1/2 -translate-y-1/2 hidden group-hover:block">
        <div className="bg-gray-800 text-white text-xs py-1 px-2 rounded-md whitespace-nowrap">
          {tooltip}
        </div>
      </div>
    )} */}

  </div>
);

function App() {
    const [isAudioRecording, setIsAudioRecording] = useState(false);
    const [isScreenRecording, setIsScreenRecording] = useState(false);
    const [isDragging, setIsDragging] = useState(false);
    const dragStartPos = useRef(null);

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
        // try {
        //     const response = await fetch(`${API_URL}/screenshot`, {
        //         method: 'POST'
        //     });
        //     const data = await response.json();
            
        //     if (data.path) {
        //         console.log('Screenshot saved:', data.path);
        //     }
        // } catch (error) {
        //     console.error('Screenshot error:', error);
        // }
        try {
            const response = await fetch(`${API_URL}/screenshot`, {  // Make sure API_URL is correct
                method: 'POST'
            });
            const data = await response.json();
            console.log("Response data:", data);  // This should show {test: 'test success!'}
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
                if (data.status === 'started') {
                    setIsScreenRecording(true);
                }
            } else {
                const response = await fetch(`${API_URL}/recording/stop`, {
                    method: 'POST'
                });
                const data = await response.json();
                if (data.status === 'stopped') {
                    setIsScreenRecording(false);
                }
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
                if (data.status === 'started') {
                    setIsAudioRecording(true);
                }
            } else {
                const response = await fetch(`${API_URL}/audio/stop`, {
                    method: 'POST'
                });
                const data = await response.json();
                if (data.status === 'stopped') {
                    setIsAudioRecording(false);
                }
            }
        } catch (error) {
            console.error('Audio recording error:', error);
        }
    };

    return (
        <div 
            className="border border-red-500 h-56 w-16 bg-white "
            onMouseDown={handleMouseDown}
        >
            <div className="flex flex-col w-full h-full p-1 gap-2 items-center justify-between">
                {/* Title bar */}
                    <div className="flex flex-row  w-full justify-center gap-1">
                        <button
                            className="cursor-pointer aspect-square transition-all duration-200 p-0.5 rounded-full text-amber-950 bg-amber-400 hover:bg-amber-500"
                            onClick={() => ipcRenderer.send('minimize-window')}
                        >
                            <Minus size={14}  />
                        </button>
                        <button
                            className="cursor-pointer aspect-square transition-all duration-200 p-0.5 rounded-full text-red-950 bg-red-400 hover:bg-red-500"
                            onClick={() => ipcRenderer.send('close-window')}
                        >

                          
                            <X size={14}  />
                        </button>
                    </div>

                {/* Main toolbar */}
                <div className="flex flex-col items-center gap-1">
                    <IconButton 
                        icon={Camera} 
                        onClick={handleScreenshot}
                        tooltip="Take Screenshot"
                    />
                    <IconButton 
                        icon={Video} 
                        onClick={handleScreenRecording}
                        isActive={isScreenRecording}
                        tooltip={isScreenRecording ? "Stop Recording" : "Start Screen Recording"}
                    />
                    <IconButton 
                        icon={Mic} 
                        onClick={handleAudioRecording}
                        isActive={isAudioRecording}
                        tooltip={isAudioRecording ? "Stop Audio" : "Start Audio Recording"}
                    />
                </div>
            </div>
        </div>
    );
}

export default App;