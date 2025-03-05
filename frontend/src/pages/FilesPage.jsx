import React, { useState, useEffect } from 'react';
import Sidebar from '../components/Sidebar';

const API_URL = 'http://localhost:5000/api';

function FilesPage() {
    const [mediaList, setMediaList] = useState([]);
    const [filteredMedia, setFilteredMedia] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [filter, setFilter] = useState('all');
    
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
            const response = await fetch(`${API_URL}/media`);
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
    
    const handleFilterChange = (e) => {
        setFilter(e.target.value);
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
        <div className="flex h-screen bg-gray-100">
            <Sidebar />
            
            <div className="flex-1 p-8 overflow-y-auto">
                <header className="flex justify-between items-center mb-8">
                    <h1 className="text-2xl font-bold">Files</h1>
                </header>
                
                <section className="bg-white p-6 rounded-lg shadow">
                    <div className="flex justify-between items-center mb-6">
                        <h2 className="text-xl font-semibold">Media Files</h2>
                        <select 
                            className="border rounded py-2 px-4 bg-white" 
                            value={filter}
                            onChange={handleFilterChange}
                        >
                            <option value="all">All</option>
                            <option value="screenshot">Screenshots</option>
                            <option value="video">Videos</option>
                            <option value="audio">Audio</option>
                        </select>
                    </div>
                    
                    {loading ? (
                        <div className="flex justify-center py-8">
                            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-green-500"></div>
                        </div>
                    ) : error ? (
                        <div className="text-red-500 text-center py-8">
                            <p>Error loading media: {error}</p>
                            <button 
                                className="mt-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                                onClick={fetchMedia}
                            >
                                Try Again
                            </button>
                        </div>
                    ) : filteredMedia.length > 0 ? (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                            {filteredMedia.map((item) => (
                                <div key={item.media_id}>
                                    {renderMediaItem(item)}
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="text-center py-8 text-gray-500">
                            <p>No media files found for this filter.</p>
                        </div>
                    )}
                </section>
            </div>
        </div>
    );
}

export default FilesPage;