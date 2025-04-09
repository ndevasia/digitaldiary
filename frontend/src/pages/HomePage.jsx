import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Plus } from 'lucide-react';
import Sidebar from '../components/Sidebar';


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
            // Use the relative URL
            const response = await fetch('/api/latest-screenshot');
            const data = await response.json();
            setScreenshotUrl(data.screenshot_url);
        } catch (error) {
            console.error('Error fetching screenshot:', error);
        } finally {
            setLoading(false);
        }
    };
    
    return (
        <div className="flex h-screen bg-blue-50">
            <Sidebar />

            <div className="flex-1 p-8 overflow-y-auto">
                <header className="flex justify-between items-center mb-6">
                    <h1 className="text-2xl font-semibold text-gray-700">Hello, User 1 & User 2</h1>
                    <button
                        onClick={() => window.electron.ipcRenderer.send('openInputWindow')}
                        className="bg-teal-500 hover:bg-teal-600 text-white px-6 py-3 rounded-full flex items-center transition-colors"
                    >
                        <Plus size={20} className="mr-2"/>
                        New Session
                    </button>
                </header>

                <section className="mb-8">
                    <h2 className="text-xl font-medium text-gray-700 mb-4">Memories</h2>

                    <div className="bg-white rounded-lg border border-gray-200 p-8">
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                            <div>
                                {loading ? (
                                    <div className="animate-pulse bg-blue-100 w-full h-64 rounded"></div>
                                ) : screenshotUrl ? (
                                    <img
                                        src={screenshotUrl}
                                        alt="Latest Screenshot"
                                        className="w-full h-64 object-cover rounded"
                                    />
                                ) : (
                                    <div className="bg-blue-100 w-full h-64 rounded flex items-center justify-center">
                                        <p className="text-gray-500 text-center">No screenshots yet</p>
                                    </div>
                                )}
                                <p className="text-center mt-2">Today</p>
                            </div>

                            <div>
                                <div className="bg-blue-100 w-full h-64 rounded"></div>
                                <p className="text-center mt-2">1 week ago</p>
                            </div>

                            <div>
                                <div className="bg-blue-100 w-full h-64 rounded"></div>
                                <p className="text-center mt-2">1 month ago</p>
                            </div>
                        </div>
                    </div>
                </section>
            </div>
        </div>
    );
}

export default HomePage;