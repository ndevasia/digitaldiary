import React, { useState, useEffect, useRef } from 'react';
import { Mic, Video, Camera, X, Minus } from 'lucide-react';
const { ipcRenderer } = window.require('electron');

const API_URL = 'http://localhost:5000/api';

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
          className="h-screen w-20 bg-transparent"
          onMouseDown={handleMouseDown}
      >

    {/* <div className="h-screen w-screen bg-transparent" style={{WebkitAppRegion:"drag"}}> */}
          {/* Centered container */}
          <div className="flex flex-col items-center h-full">
              {/* Close button at top */}
              <div className="w-full flex justify-end p-2">
                  <button
                      className="w-6 h-6 bg-transparent hover:bg-red-500 rounded-full flex items-center justify-center"
                      onClick={() => ipcRenderer.send('close-window')}
                  >
                      <X className="text-black hover:text-white" size={14} />
                  </button>
                  

                  
              </div>
              <button
                      className="w-6 h-6 bg-transparent hover:bg-red-500 rounded-full flex items-center justify-center"
                      onClick={() => ipcRenderer.send('minimize-window')}
                  >
                      <Minus className="text-black hover:text-white" size={14} />

                  </button>

              {/* Icons stack vertically */}
              <div className="flex flex-col gap-8 mt-4">
                  <button
                      onClick={handleScreenshot}
                      className="w-10 h-10 bg-transparent hover:bg-white hover:bg-opacity-10 rounded-full flex items-center justify-center"
                  >
                      <Camera size={24} className="text-black" />
                  </button>

                  <button
                      onClick={handleScreenRecording}
                      className="w-10 h-10 bg-transparent hover:bg-white hover:bg-opacity-10 rounded-full flex items-center justify-center"
                  >
                      <Video size={24} className={isScreenRecording ? "text-red-500" : "text-black"} />
                  </button>

                  <button
                      onClick={handleAudioRecording}
                      className="w-10 h-10 bg-transparent hover:bg-white hover:bg-opacity-10 rounded-full flex items-center justify-center"
                  >
                      <Mic size={24} className={isAudioRecording ? "text-red-500" : "text-black"} />
                  </button>
              </div>
          </div>
      </div>
  );
}

export default App;