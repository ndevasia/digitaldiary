import { useRef, useState, useMemo } from 'react';
import { Play, Pause, Volume2, VolumeX, Download } from 'lucide-react';

export default function AudioPlayer({ src }) {
    const audioRef = useRef(null);
    
    const [isPlaying, setIsPlaying] = useState(false);
    const [progress, setProgress] = useState(0);
    const [playbackRate, setPlaybackRate] = useState(1);
    const [isMuted, setIsMuted] = useState(false);
    
    // Added state for timestamps
    const [currentTime, setCurrentTime] = useState(0);
    const [duration, setDuration] = useState(0);

    const speeds = [0.75, 1, 1.25, 1.5, 2];
    const cycleSpeed = () => {
        if (audioRef.current) {
            const nextIndex = (speeds.indexOf(playbackRate) + 1) % speeds.length;
            const newSpeed = speeds[nextIndex];
            audioRef.current.playbackRate = newSpeed;
            setPlaybackRate(newSpeed);
        }
    };

    const togglePlay = () => {
        if (audioRef.current) {
            if (isPlaying) audioRef.current.pause();
            else audioRef.current.play();
            setIsPlaying(!isPlaying);
        }
    };

    const handleLoadedMetadata = () => {
        if (audioRef.current) setDuration(audioRef.current.duration);
    };

    const handleTimeUpdate = () => {
        const audio = audioRef.current;
        if (audio && audio.duration) {
            setCurrentTime(audio.currentTime);
            setProgress((audio.currentTime / audio.duration) * 100);
        }
    };

    const handleSeek = (e) => {
        const audio = audioRef.current;
        if (audio && audio.duration) {
            const newPercentage = e.target.value;
            const newTime = (newPercentage / 100) * audio.duration;
            audio.currentTime = newTime;
            setCurrentTime(newTime);
            setProgress(newPercentage);
        }
    };

    const toggleMute = () => {
        if (audioRef.current) {
            audioRef.current.muted = !isMuted;
            setIsMuted(!isMuted);
        }
    };

    const formatTime = (timeInSeconds) => {
        if (isNaN(timeInSeconds)) return "0:00";
        const minutes = Math.floor(timeInSeconds / 60);
        const seconds = Math.floor(timeInSeconds % 60);
        return `${minutes}:${seconds.toString().padStart(2, '0')}`;
    };

    // Generating randomness in waveform bars
    // Will stay consistent for the same session but different after reload
    // due to s3 presigned urls
    const bars = useMemo(() => {
        const safeSrc = String(src || 'default'); 
        let hash = 0;
        for (let i = 0; i < safeSrc.length; i++) {
            hash = safeSrc.charCodeAt(i) + ((hash << 5) - hash);
        }
        let seed = Math.abs(hash) || 12345; 

        return Array.from({ length: 15 }, () => {
            const x = Math.sin(seed++) * 10000;
            const random = x - Math.floor(x);
            // Map to a scale factor between 0.2 and 1.0
            const scale = (random * 0.8) + 0.2; 
            const delay = random * 0.8; 
            return { scale, delay };
        });
    }, [src]);

    return (
        <div className="w-full h-[160px] bg-white border border-teal-200 rounded flex flex-col p-4 shadow-sm relative">
            
            <style>{`
                @keyframes dynamic-bounce {
                    0%, 100% { transform: scaleY(1); }
                    50% { transform: scaleY(var(--min-scale)); } 
                }
            `}</style>

            <audio
                ref={audioRef}
                src={src}
                onLoadedMetadata={handleLoadedMetadata}
                onTimeUpdate={handleTimeUpdate}
                onEnded={() => setIsPlaying(false)}
            />

            {/* Top: Fake Waveform */}
            <div className="flex-1 w-full bg-gray-100 rounded mb-3 overflow-hidden border border-gray-200 relative">
                <div className="absolute inset-0 flex items-center justify-center gap-1">
                    {bars.map((bar, i) => (
                        <div 
                            key={i}
                            className="w-1 h-[60%] bg-teal-500 rounded-full origin-center"
                            style={{
                                '--min-scale': bar.scale,
                                animation: isPlaying 
                                    ? `dynamic-bounce 0.8s infinite ease-in-out ${bar.delay}s` 
                                    : 'none',
                                // When paused, show them staggered
                                transform: `scaleY(${bar.scale})` 
                            }}
                        />
                    ))}
                </div>
            </div>

            {/* Bottom: Controls */}
            <div className="flex flex-col gap-2">
                <div className="flex items-center justify-between mb-1">
                    <button 
                        onClick={togglePlay} 
                        className="text-gray-700 hover:text-teal-600 transition-colors"
                    >
                        {isPlaying ? <Pause size={20} /> : <Play size={20} />}
                    </button>
                    
                    <button 
                        onClick={cycleSpeed}
                        className="text-xs font-semibold text-gray-600 hover:text-teal-600 w-8 text-right transition-colors"
                    >
                        {playbackRate}x
                    </button>
                </div>

                <input
                    type="range"
                    min="0"
                    max="100"
                    value={progress || 0}
                    onChange={handleSeek}
                    className="w-full h-1.5 rounded-full appearance-none cursor-pointer accent-teal-500 hover:accent-teal-400 bg-gray-200"
                    style={{
                        background: `linear-gradient(to right, #14b8a6 ${progress}%, #e5e7eb ${progress}%)`
                    }}
                />

                <div className="flex items-center justify-between text-gray-400 mt-1 ml-0.5 text-xs">
                    <div className="flex items-center gap-3">
                        <button 
                            onClick={toggleMute}
                            className="hover:text-teal-600 transition-colors text-gray-500"
                        >
                            {isMuted ? <VolumeX size={16} /> : <Volume2 size={16} />}
                        </button>
                        
                        {/* Timestamps */}
                        <span className="font-medium tracking-wide">
                            {formatTime(currentTime)} / {formatTime(duration)}
                        </span>
                    </div>

                    <a 
                        href={src} 
                        download 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="hover:text-teal-600 transition-colors text-gray-500"
                    >
                        <Download size={16} />
                    </a>
                </div>
            </div>
        </div>
    );
}