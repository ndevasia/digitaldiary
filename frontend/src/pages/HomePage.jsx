import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Sidebar from '../components/Sidebar';

const API_URL = 'http://localhost:5000/api';

function HomePage() {
    const [screenshotUrl, setScreenshotUrl] = useState(null);
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
        // Fetch the latest screenshot when component mounts
        fetchLatestScreenshot();
    }, []);
    
    const fetchLatestScreenshot = async () => {
        try {
            setLoading(true);
            const response = await fetch(`${API_URL}/latest-screenshot`);
            const data = await response.json();
            setScreenshotUrl(data.screenshot_url);
        } catch (error) {
            console.error('Error fetching screenshot:', error);
        } finally {
            setLoading(false);
        }
    };
    
    return (
        <div className="flex h-screen bg-gray-100">
            <Sidebar />
            
            <div className="flex-1 p-8">
                <header className="flex justify-between items-center mb-8">
                    <h1 className="text-2xl font-bold">Hello, User 1 & User 2</h1>
                    <button className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 transition-colors">
                        + New Session
                    </button>
                </header>
                
                <section className="bg-white p-6 rounded-lg shadow">
                    <h2 className="text-xl font-semibold mb-4">Memories</h2>
                    
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                        <div className="col-span-1 flex items-center justify-center">
                            {loading ? (
                                <div className="animate-pulse bg-gray-200 w-full h-48 rounded"></div>
                            ) : screenshotUrl ? (
                                <img 
                                    src={screenshotUrl} 
                                    alt="Latest Screenshot" 
                                    className="max-w-full h-auto rounded shadow-sm"
                                />
                            ) : (
                                <div className="text-center p-6 bg-gray-100 rounded">
                                    <p>No screenshots available yet.</p>
                                    <p>Take one to see it here!</p>
                                </div>
                            )}
                        </div>
                        
                        <div className="bg-blue-100 p-4 rounded text-center">
                            <h3 className="font-medium">1 week ago</h3>
                        </div>
                        
                        <div className="bg-blue-100 p-4 rounded text-center">
                            <h3 className="font-medium">1 month ago</h3>
                        </div>
                        
                        <div className="bg-blue-100 p-4 rounded text-center">
                            <h3 className="font-medium">1 year ago</h3>
                        </div>
                    </div>
                </section>
            </div>
        </div>
    );
}

export default HomePage;