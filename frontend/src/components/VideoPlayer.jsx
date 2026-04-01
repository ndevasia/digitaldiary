import { useRef, useState, useEffect } from 'react';
import { Pause, Play, Maximize, Minimize, Volume2, VolumeX, Download } from 'lucide-react';

// Time formatting for timestamps
const formatTime = (timeInSeconds) => {
    if (isNaN(timeInSeconds)) return "0:00";
    const minutes = Math.floor(timeInSeconds / 60);
    const seconds = Math.floor(timeInSeconds % 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
};

export default function VideoPlayer({ src }) {
    const videoRef = useRef(null);
    
    const [isPlaying, setIsPlaying] = useState(false);
    const [progress, setProgress] = useState(0);
    const [currentTime, setCurrentTime] = useState(0);
    const [duration, setDuration] = useState(0);
    const [playbackRate, setPlaybackRate] = useState(1);
    const [showSpeedMenu, setShowSpeedMenu] = useState(false);
    const [isExpanded, setIsExpanded] = useState(false);
    const [isFading, setIsFading] = useState(false);
    const [volume, setVolume] = useState(1);
    const [isMuted, setIsMuted] = useState(false);

    // Play/pause
    const togglePlay = () => {
        if (videoRef.current) {
            if (isPlaying) videoRef.current.pause();
            else videoRef.current.play();
            setIsPlaying(!isPlaying);
        }
    };

    // Metadata needs to be loaded to check duration
    const handleLoadedMetadata = () => {
        if (videoRef.current) setDuration(videoRef.current.duration);
    };

    // Update progress as video plays
    const handleTimeUpdate = () => {
        const video = videoRef.current;
        if (video && video.duration) {
            setCurrentTime(video.currentTime);
            setProgress((video.currentTime / video.duration) * 100);
        }
    };

    // Seeking
    const handleSeek = (e) => {
        const video = videoRef.current;
        if (video && video.duration) {
            const newPercentage = e.target.value; 
            const newTime = (newPercentage / 100) * video.duration; 
            video.currentTime = newTime; 
            setProgress(newPercentage); 
            setCurrentTime(newTime);
        }
    };

    // Mute/unmute
    const toggleVolume = () => {
        if (videoRef.current) {
            videoRef.current.muted = !isMuted;
            setIsMuted(!isMuted);
        }
    };

    // Change playback speed
    const handleSpeedChange = (rate) => {
        if (videoRef.current) {
            videoRef.current.playbackRate = rate;
            setPlaybackRate(rate);
            setShowSpeedMenu(false);
        }
    };

    // Time buffer for animation of entering fullscreen
    const openFullscreen = () => {
        setIsExpanded(true);
        setTimeout(() => setIsFading(true), 10);
    };

    // Time buffer for exiting fullscreen
    const closeFullscreen = () => {
        setIsFading(false);
        setTimeout(() => setIsExpanded(false), 300);
    };

    const toggleFullscreen = () => {
        if (!isExpanded) openFullscreen();
        else closeFullscreen();
    };

    // Lets you close fullscreen by clicking outside of player
    const handleBackgroundClick = (e) => {
        if (isExpanded && e.target === e.currentTarget) {
            closeFullscreen();
        }
    };

    // --- Keyboard Shortcuts & Overflow ---
    // Escape to exit fullscreen, Space to play/pause, M to mute/unmute, Arrow keys to seek
    useEffect(() => {
        const handleKeyDown = (e) => {
            if (isExpanded && videoRef.current) {
                if (e.key === 'Escape') closeFullscreen();
                
                if (e.key === 'm' || e.key === 'M') {
                    videoRef.current.muted = !videoRef.current.muted;
                    setIsMuted(videoRef.current.muted);
                }
                
                if (e.code === 'Space') {
                    e.preventDefault(); 
                    if (videoRef.current.paused) {
                        videoRef.current.play();
                        setIsPlaying(true);
                    } else {
                        videoRef.current.pause();
                        setIsPlaying(false);
                    }
                }

                if (e.code === 'ArrowRight') {
                    e.preventDefault(); 
                    videoRef.current.currentTime = Math.min(videoRef.current.duration, videoRef.current.currentTime + 5);
                }

                if (e.code === 'ArrowLeft') {
                    e.preventDefault(); 
                    videoRef.current.currentTime = Math.max(0, videoRef.current.currentTime - 5);
                }
            }
        };
        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [isExpanded]);

    // Prevent background scrolling when in fullscreen
    useEffect(() => {
        if (isExpanded) document.body.style.overflow = 'hidden';
        else document.body.style.overflow = 'unset';
        return () => { document.body.style.overflow = 'unset'; };
    }, [isExpanded]);

    // Dynamic CSS Classes with Fade
    const containerClasses = isExpanded
        ? `fixed inset-0 z-50 flex items-center justify-center bg-black/95 backdrop-blur-md p-4 md:p-10 group transition-all duration-500 ease-out ${isFading ? 'opacity-100' : 'opacity-0'}`
        : "relative group w-full bg-black rounded overflow-hidden shadow-sm hover:shadow-md transition-shadow duration-500 opacity-100";

    // Added a subtle scale effect alongside the fade
    const innerWrapperClasses = `relative transition-transform duration-100 ease-out ${
        isExpanded 
            ? `w-full max-w-5xl ${isFading ? 'scale-100' : 'scale-75'}` 
            : 'w-full scale-100'
    }`;

    return (
        <div className={containerClasses} onClick={handleBackgroundClick}>
            
            <div className={innerWrapperClasses}>
                
                <video
                    ref={videoRef}
                    className={isExpanded ? "w-full max-w-5xl h-auto max-h-[85vh] object-contain" : "w-full h-auto"}
                    onTimeUpdate={handleTimeUpdate}
                    onLoadedMetadata={handleLoadedMetadata}
                    src={src}
                />

                {/* Top-Left Timestamp */}
                {!isExpanded && (
                    <div className="absolute top-2 left-2 bg-teal-700/50 text-white text-xs font-medium px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none tracking-wide z-10">
                        {formatTime(currentTime)} / {formatTime(duration)}
                    </div>
                )}

                {/* Top-Right Expand/Minimize Button */}
                <button
                    onClick={toggleFullscreen}
                    className="absolute top-1.5 right-2 bg-teal-700/50 text-white p-1.5 rounded opacity-0 group-hover:opacity-100 transition-opacity duration-300 hover:text-teal-400 z-20"
                    aria-label={isExpanded ? "Close fullscreen" : "Expand video"}
                >
                    {isExpanded ? <Minimize size={16} /> : <Maximize size={16} />}
                </button>

                {/* Bottom Controls Bar */}
                <div className={`absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 z-10 ${isExpanded ? 'p-4 flex flex-col gap-2' : 'p-3 flex items-center gap-3'}`}>
                    
                    {/* Progress Bar */}
                    <input
                        type="range"
                        min="0"
                        max="100"
                        value={progress || 0}
                        onChange={handleSeek}
                        className={`${isExpanded ? 'w-full' : 'flex-1 order-last'} h-1.5 rounded-full appearance-none cursor-pointer accent-teal-500 hover:accent-teal-400 transition-all`}
                        style={{
                            background: `linear-gradient(to right, #14b8a6 ${progress}%, rgba(107, 114, 128, 0.5) ${progress}%)`
                        }}
                    />

                    {/* Controls Row */}
                    <div className={`flex items-center ${isExpanded ? 'justify-between mt-2' : 'gap-3 order-first'}`}>
                        
                        {/* LEFT SIDE */}
                        <div className="flex items-center gap-4">
                            <button onClick={togglePlay} className="text-white hover:text-teal-400 transition-colors">
                                {isPlaying ? <Pause size={isExpanded ? 24 : 20} /> : <Play size={isExpanded ? 24 : 20} />}
                            </button>

                            {isExpanded && (
                                <>
                                    <button onClick={toggleVolume} className="text-white hover:text-teal-400 transition-colors">
                                        {isMuted || volume === 0 ? <VolumeX size={20} /> : <Volume2 size={20} />}
                                    </button>
                                    <div className="text-white text-sm font-medium tracking-wide">
                                        {formatTime(currentTime)} <span className="text-gray-400 mx-1">/</span> {formatTime(duration)}
                                    </div>
                                </>
                            )}
                        </div>

                        {/* RIGHT SIDE */}
                        {isExpanded && (
                            <div className="flex items-center gap-5 relative">
                                {/* Speed Menu */}
                                <div className="relative flex items-center">
                                    {showSpeedMenu && (
                                        <div className="absolute bottom-full mb-3 left-1/2 -translate-x-1/2 bg-black/90 rounded-md overflow-hidden flex flex-col py-1 border border-gray-700/50 shadow-xl">
                                            {[0.5, 1, 1.25, 1.5, 2].map((rate) => (
                                                <button
                                                    key={rate}
                                                    onClick={(e) => {
                                                        e.stopPropagation();
                                                        handleSpeedChange(rate);
                                                    }}
                                                    className={`px-4 py-1.5 text-sm hover:bg-teal-700/50 transition-colors whitespace-nowrap ${
                                                        playbackRate === rate ? 'text-teal-400 font-bold' : 'text-white'
                                                    }`}
                                                >
                                                    {rate}x
                                                </button>
                                            ))}
                                        </div>
                                    )}
                                    <button 
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            setShowSpeedMenu(!showSpeedMenu);
                                        }}
                                        className="text-white hover:text-teal-400 font-medium text-sm transition-colors min-w-[3ch]"
                                    >
                                        {playbackRate}x
                                    </button>
                                </div>

                                {/* Download */}
                                <a 
                                    href={src} download target="_blank" rel="noopener noreferrer"
                                    onClick={(e) => e.stopPropagation()}
                                    className="text-white hover:text-teal-400 transition-colors"
                                >
                                    <Download size={20} />
                                </a>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}