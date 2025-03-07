import React, { useState, useEffect } from 'react';
import { ChevronDown } from 'lucide-react';
import Sidebar from '../components/Sidebar';

function FilesPage() {
    const [mediaList, setMediaList] = useState([]);
    const [filteredMedia, setFilteredMedia] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [filter, setFilter] = useState('all');
    const [showDropdown, setShowDropdown] = useState(false);
    
    
    useEffect(() => {
        fetchMedia();
    }, []);
    
    useEffect(() => {
        if (filter === 'all') {
            setFilteredMedia(mediaList);
        } else {
            setFilteredMedia(mediaList.filter(item => item.type === filter));
        }
    }, [filter, mediaList]);
    
    const fetchMedia = async () => {
        try {
            setLoading(true);
            const response = await fetch(`/api/media`);
            if (!response.ok) {
                throw new Error('Failed to fetch media');
            }
            const data = await response.json();
            setMediaList(data);
            setFilteredMedia(data);
        } catch (error) {
            console.error('Error fetching media:', error);
            setError(error.message);
        } finally {
            setLoading(false);
        }
    };
    
    const handleFilterChange = (filterType) => {
        setFilter(filterType);
        setShowDropdown(false);
    };


    const renderMediaItem = (item) => {
        switch (item.type) {
            case 'video':
                return (
                    <div className="media-item p-4 bg-white rounded shadow-sm">
                        <video controls className="w-full rounded mb-2">
                            <source src={item.media_url} type="video/mp4" />
                            Your browser does not support the video tag.
                        </video>
                        <p className="font-medium">{item.game}</p>
                    </div>
                );
            case 'audio':
                return (
                    <div className="media-item p-4 bg-white rounded shadow-sm">
                        <audio controls className="w-full mb-2">
                            <source src={item.media_url} type="audio/mpeg" />
                            Your browser does not support the audio tag.
                        </audio>
                        <p className="font-medium">{item.game}</p>
                    </div>
                );
            case 'screenshot':
                return (
                    <div className="media-item p-4 bg-white rounded shadow-sm">
                        <img src={item.media_url} alt="Screenshot" className="w-full rounded mb-2" />
                        <p className="font-medium">{item.game}</p>
                    </div>
                );
            default:
                return null;
        }
    };
    
    return (
        <div className="flex h-screen bg-blue-50">
            <Sidebar />
            
            <div className="flex-1 p-8 overflow-y-auto">
                <header className="flex justify-between items-center mb-6">
                    <h1 className="text-2xl font-semibold text-gray-700">Hello, User 1 & User 2</h1>
                </header>
                
                <section className="mb-8">
                    <h2 className="text-xl font-medium text-gray-700 mb-4">Files</h2>
                    
                    <div className="bg-white rounded-lg border border-gray-200 p-8">
                        <div className="relative flex justify-end mb-4">
                            <button 
                                className="bg-teal-500 text-white px-4 py-2 rounded flex items-center"
                                onClick={() => setShowDropdown(!showDropdown)}
                            >
                                Sort by <ChevronDown size={18} className="ml-2" />
                            </button>
                            
                            {showDropdown && (
                                <div className="absolute top-full right-0 mt-1 bg-white shadow-md rounded-lg border border-gray-200 w-40 z-10">
                                    <ul>
                                        <li className="px-4 py-2 hover:bg-gray-100 text-teal-500 cursor-pointer" onClick={() => handleFilterChange('screenshot')}>
                                            Screenshots
                                        </li>
                                        <li className="px-4 py-2 hover:bg-gray-100 text-teal-500 cursor-pointer" onClick={() => handleFilterChange('audio')}>
                                            Audio
                                        </li>
                                        <li className="px-4 py-2 hover:bg-gray-100 text-teal-500 cursor-pointer" onClick={() => handleFilterChange('video')}>
                                            Video
                                        </li>
                                    </ul>
                                </div>
                            )}
                        </div>
                        
                        {loading ? (
                            <div className="grid grid-cols-3 gap-6">
                                {[1, 2, 3, 4, 5, 6].map((_, index) => (
                                    <div key={index} className="animate-pulse bg-blue-100 h-48 rounded"></div>
                                ))}
                            </div>
                        ) : error ? (
                            <div className="text-center py-12">
                                <p className="text-red-500">{error}</p>
                                <button 
                                    className="mt-4 bg-teal-500 text-white px-4 py-2 rounded hover:bg-teal-600"
                                    onClick={fetchMedia}
                                >
                                    Try Again
                                </button>
                            </div>
                        ) : filteredMedia.length === 0 ? (
                            <div className="text-center py-12">
                                <p className="text-gray-500">No media files found.</p>
                            </div>
                        ) : (
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                                {filteredMedia.map((item) => {
                                    let mediaClass = '';
                                    
                                    switch(item.type) {
                                        case 'video':
                                            mediaClass = 'bg-pink-200';
                                            break;
                                        case 'screenshot':
                                            mediaClass = 'bg-blue-100';
                                            break;
                                        case 'audio':
                                            mediaClass = 'bg-green-200';
                                            break;
                                        default:
                                            mediaClass = 'bg-blue-100';
                                    }
                                    
                                    return (
                                        <div 
                                            key={item.media_id} 
                                            className={`${mediaClass} h-48 rounded flex items-center justify-center`}
                                        >
                                            {renderMediaItem(item)}
                                        </div>
                                    );
                                })}
                            </div>
                        )}
                    </div>
                </section>
            </div>
        </div>
    );
}

export default FilesPage;