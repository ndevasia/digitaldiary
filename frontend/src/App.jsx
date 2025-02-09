import React, { useState, useEffect, useRef } from 'react';
import { Mic, Video, Camera, X, Minus } from 'lucide-react';
const { ipcRenderer } = window.require('electron');

const API_URL = 'http://localhost:5000/api';

const IconButton = ({ icon: Icon, onClick, isActive, tooltip }) => (
  <div className="relative group">
    <button
      onClick={onClick}
      className={`w-10 h-10 rounded-lg flex items-center justify-center transition-all duration-200 ${
        isActive 
          ? 'bg-white bg-opacity-20 shadow-lg' 
          : 'bg-transparent hover:bg-white hover:bg-opacity-10'
      }`}
    >
      <Icon 
        size={20} 
        className={`${isActive ? 'text-red-500' : 'text-gray-800'} transition-colors duration-200`} 
      />
    </button>
    {/* {tooltip && (
      <div className="absolute left-12 top-1/2 -translate-y-1/2 hidden group-hover:block">
        <div className="bg-gray-800 text-white text-xs py-1 px-2 rounded-md whitespace-nowrap">
          {tooltip}
        </div>
      </div>
    )} */}
    <div className="h-6" /> {/* This creates the line break space */}
    

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
        try {
            const response = await fetch(`${API_URL}/screenshot`, {
                method: 'POST'
            });
            const data = await response.json();
            if (data.path) {
                console.log('Screenshot saved:', data.path);
            }
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
            className="h-screen w-24 bg-white bg-opacity-5 backdrop-blur-sm"
            onMouseDown={handleMouseDown}
        >
            <div className="flex flex-col w-full h-full">
                {/* Title bar */}
                <div className="flex justify-end p-1">
                    <div className="flex flex-row item-">
                        <button
                            className="w-2 h-2 rounded-full inline-flex items-center justify-center hover:bg-gray-200 hover:bg-opacity-20 transition-colors"
                            onClick={() => ipcRenderer.send('minimize-window')}
                        >
                          <span className="text-red-500">test</span>
                            <Minus size={8} className="text-gray-600" />
                        </button>
                        <button
                            className="w-2 h-2 rounded-full inline-flex items-center justify-center hover:bg-red-500 transition-colors"
                            onClick={() => ipcRenderer.send('close-window')}
                        >
                            <X size={8} className="text-gray-600 hover:text-white" />
                        </button>
                    </div>
                </div>

                {/* Main toolbar */}
                <div className="flex-1 flex flex-col items-center pt-2 gap-4">
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