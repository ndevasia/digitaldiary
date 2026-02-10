import React, { useState, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, ChevronLeft } from 'lucide-react';
import HeroImage from '../components/HeroImage';
import Timeline from '../components/Timeline';
import { UserContext } from '../context/UserContext.jsx';

function HomePage() {
    const [screenshotUrl, setScreenshotUrl] = useState(null);
    const [oneWeekAgoScreenshotUrl, setOneWeekAgoScreenshotUrl] = useState(null);
    const [oneMonthAgoScreenshotUrl, setOneMonthAgoScreenshotUrl] = useState(null);
    const [loading, setLoading] = useState(true);
    const [loadingOneWeekAgo, setLoadingOneWeekAgo] = useState(true);
    const [loadingOneMonthAgo, setLoadingOneMonthAgo] = useState(true);
    const [selectedTimeframe, setSelectedTimeframe] = useState(null);
    const [showModal, setShowModal] = useState(false);
    const [modalImage, setModalImage] = useState('');
    const [gameEvents, setGameEvents] = useState([]);
    const [loadingTimeline, setLoadingTimeline] = useState(true);
    const navigate = useNavigate();
    const currentUsername = useContext(UserContext).username || 'User';

    useEffect(() => {
        // Fetch the latest screenshot when component mounts
        fetchLatestScreenshot();
        // Fetch the one week ago screenshot
        fetchScreenshotByDays(7, setOneWeekAgoScreenshotUrl, setLoadingOneWeekAgo);
        // Fetch the one month ago screenshot
        fetchScreenshotByDays(30, setOneMonthAgoScreenshotUrl, setLoadingOneMonthAgo);
        // Fetch game sessions
        fetchGameSessions();
    }, []);

    const fetchLatestScreenshot = async () => {
        try {
            setLoading(true);
            const response = await fetch('/api/latest-screenshot');
            const data = await response.json();
            setScreenshotUrl(data.screenshot_url);
        } catch (error) {
            console.error('Error fetching screenshot:', error);
        } finally {
            setLoading(false);
        }
    };

    const fetchScreenshotByDays = async (days, setScreenshotUrl, setLoading) => {
        try {
            setLoading(true);
            const response = await fetch(`/api/random-screenshot-by-days/${days}`);
            const data = await response.json();
            setScreenshotUrl(data.screenshot_url);
        } catch (error) {
            console.error(`Error fetching screenshot from ${days} days ago:`, error);
        } finally {
            setLoading(false);
        }
    };

    const fetchGameSessions = async () => {
        try {
            setLoadingTimeline(true);
            const response = await fetch('/api/media_aws');
            const mediaData = await response.json();

            // Group media by game_id and get the latest timestamp for each game
            const gameSessions = mediaData.reduce((acc, item) => {
                if (!item.game_id) return acc;

                const gameId = item.game_id;
                const timestamp = new Date(item.timestamp);

                if (!acc[gameId] || timestamp > acc[gameId].timestamp) {
                    acc[gameId] = {
                        title: `Game ${gameId}`,
                        date: timestamp.toLocaleDateString(),
                        timestamp: timestamp
                    };
                }

                return acc;
            }, {});

            // Convert to array and sort by timestamp
            const timeline = Object.values(gameSessions)
                .sort((a, b) => b.timestamp - a.timestamp);

            setGameEvents(timeline);
        } catch (error) {
            console.error('Error fetching game sessions:', error);
        } finally {
            setLoadingTimeline(false);
        }
    };

    const handleTimeframeClick = (timeframe) => {
        setSelectedTimeframe(timeframe);
    };

    const handleBackClick = () => {
        setSelectedTimeframe(null);
    };

    const enlargeImage = (imageUrl) => {
        setModalImage(imageUrl);
        setShowModal(true);
    };

    const closeModal = () => {
        setShowModal(false);
    };

    const handleHeroImageChange = (newImageUrl) => {
        // This function is called when the hero image changes
        console.log('Hero image changed:', newImageUrl);
    };

    // Render the memories list
    const renderMemoriesList = () => {
        return (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div
                    className="cursor-pointer"
                    onClick={() => handleTimeframeClick('today')}
                >
                    {loading ? (
                        <div className="animate-pulse bg-blue-100 w-full h-64 rounded"></div>
                    ) : screenshotUrl ? (
                        <div className="bg-white rounded-lg border border-gray-200 overflow-hidden shadow-sm transition-all hover:shadow-md hover:-translate-y-1">
                            <img
                                src={screenshotUrl}
                                alt="Latest Screenshot"
                                className="w-full h-64 object-cover"
                            />
                            <div className="p-4">
                                <p className="text-center font-medium text-gray-700">Today</p>
                            </div>
                        </div>
                    ) : (
                        <div className="bg-blue-100 w-full h-64 rounded flex items-center justify-center">
                            <p className="text-gray-500 text-center">No screenshots yet</p>
                        </div>
                    )}
                </div>

                <div
                    className="cursor-pointer"
                    onClick={() => handleTimeframeClick('oneWeekAgo')}
                >
                    {loadingOneWeekAgo ? (
                        <div className="animate-pulse bg-blue-100 w-full h-64 rounded"></div>
                    ) : oneWeekAgoScreenshotUrl ? (
                        <div className="bg-white rounded-lg border border-gray-200 overflow-hidden shadow-sm transition-all hover:shadow-md hover:-translate-y-1">
                            <img
                                src={oneWeekAgoScreenshotUrl}
                                alt="One Week Ago Screenshot"
                                className="w-full h-64 object-cover"
                            />
                            <div className="p-4">
                                <p className="text-center font-medium text-gray-700">1 week ago</p>
                            </div>
                        </div>
                    ) : (
                        <div className="bg-blue-100 w-full h-64 rounded flex items-center justify-center">
                            <p className="text-gray-500 text-center">No screenshots from a week ago</p>
                        </div>
                    )}
                </div>

                <div
                    className="cursor-pointer"
                    onClick={() => handleTimeframeClick('oneMonthAgo')}
                >
                    {loadingOneMonthAgo ? (
                        <div className="animate-pulse bg-blue-100 w-full h-64 rounded"></div>
                    ) : oneMonthAgoScreenshotUrl ? (
                        <div className="bg-white rounded-lg border border-gray-200 overflow-hidden shadow-sm transition-all hover:shadow-md hover:-translate-y-1">
                            <img
                                src={oneMonthAgoScreenshotUrl}
                                alt="One Month Ago Screenshot"
                                className="w-full h-64 object-cover"
                            />
                            <div className="p-4">
                                <p className="text-center font-medium text-gray-700">1 month ago</p>
                            </div>
                        </div>
                    ) : (
                        <div className="bg-blue-100 w-full h-64 rounded flex items-center justify-center">
                            <p className="text-gray-500 text-center">No screenshots from a month ago</p>
                        </div>
                    )}
                </div>
            </div>
        );
    };

    // Render the timeframe detail view
    const renderTimeframeDetail = () => {
        if (!selectedTimeframe) return null;

        const timeframeTitles = {
            today: "Today's Screenshots",
            oneWeekAgo: "Screenshots from a Week Ago",
            oneMonthAgo: "Screenshots from a Month Ago"
        };

        const currentScreenshotUrl = selectedTimeframe === 'today' ? screenshotUrl :
                            selectedTimeframe === 'oneWeekAgo' ? oneWeekAgoScreenshotUrl :
                            oneMonthAgoScreenshotUrl;

        return (
            <div>
                <div className="mb-6">
                    <button
                        onClick={handleBackClick}
                        className="flex items-center text-teal-500 hover:text-teal-600 transition-colors"
                    >
                        <ChevronLeft size={20} className="mr-1" />
                        Back to Memories
                    </button>
                </div>

                <h3 className="text-xl font-semibold text-gray-700 mb-4">{timeframeTitles[selectedTimeframe]}</h3>

                <div className="bg-white rounded-lg border border-gray-200 p-8">
                    {currentScreenshotUrl ? (
                        <div className="bg-blue-100 rounded overflow-hidden shadow-sm">
                            <div className="p-4">
                                <img
                                    src={currentScreenshotUrl}
                                    alt="Screenshot"
                                    className="w-full rounded cursor-pointer hover:opacity-90 transition-opacity"
                                    onClick={() => enlargeImage(currentScreenshotUrl)}
                                />
                                <div className="mt-2">
                                    <div className="font-medium text-gray-700">{timeframeTitles[selectedTimeframe]}</div>
                                    <div className="text-xs text-gray-500">
                                        {selectedTimeframe === 'today' ? 'Today' :
                                         selectedTimeframe === 'oneWeekAgo' ? '1 week ago' :
                                         '1 month ago'}
                                    </div>
                                </div>
                            </div>
                        </div>
                    ) : (
                        <div className="text-center py-12">
                            <p className="text-gray-500">No screenshots available for this timeframe.</p>
                        </div>
                    )}
                </div>
            </div>
        );
    };

    // Image Modal/Lightbox
    const renderImageModal = () => {
        if (!showModal) return null;

        return (
            <div
                className="fixed inset-0 bg-black bg-opacity-90 flex items-center justify-center z-50"
                onClick={closeModal}
            >
                <div
                    className="relative max-w-4xl max-h-[90vh]"
                    onClick={e => e.stopPropagation()}
                >
                    <button
                        className="absolute -top-10 -right-10 text-white text-3xl font-bold w-8 h-8 flex items-center justify-center"
                        onClick={closeModal}
                    >
                        &times;
                    </button>
                    <img
                        src={modalImage}
                        alt="Enlarged screenshot"
                        className="max-w-full max-h-[90vh] object-contain"
                    />
                </div>
            </div>
        );
    };

    return (
        <div className="flex-1 p-8 overflow-y-auto">
            <header className="flex justify-between items-center mb-6">
                <h1 className="text-2xl font-semibold text-gray-700">Hello, {currentUsername}</h1>
                <button className="bg-teal-500 hover:bg-teal-600 text-white px-6 py-3 rounded-full flex items-center transition-colors">
                    <Plus size={20} className="mr-2" />
                    New Memory
                </button>
            </header>

            {/* Hero Image */}
            <div className="mb-8">
                <HeroImage onImageChange={handleHeroImageChange} />
            </div>

            {/* Main Content */}
            <main>
                {selectedTimeframe ? renderTimeframeDetail() : renderMemoriesList()}
            </main>

            {/* Image Modal */}
            {renderImageModal()}

            {/* Timeline Section */}
            <div className="max-w-7xl mx-auto px-4 py-8">
                <h2 className="text-2xl font-bold text-teal-700 mb-6">Recent Activity</h2>
                {loadingTimeline ? (
                    <div className="animate-pulse bg-white rounded-lg border border-gray-200 p-6">
                        <div className="space-y-4">
                            {[1, 2, 3].map((i) => (
                                <div key={i} className="h-16 bg-gray-200 rounded"></div>
                            ))}
                        </div>
                    </div>
                ) : (
                    <Timeline events={gameEvents} />
                )}
            </div>
        </div>
    );
}

export default HomePage;