import React, { useState, useEffect, useContext, useRef } from 'react';
import { BarChart2 } from 'lucide-react';
import Timeline from '../components/Timeline';
import { UserContext } from '../context/UserContext.jsx';

function StatsPage() {
    const user = useContext(UserContext);
    const currentUsername = user?.username || 'User';
    const apiBasePath = `/api/${encodeURIComponent(currentUsername)}`;

    const [mediaStats, setMediaStats] = useState({
        screenshots: 0,
        videos: 0,
        audio: 0
    });
    const [loadingStats, setLoadingStats] = useState(true);
    const [gameEvents, setGameEvents] = useState([]);
    const [loadingTimeline, setLoadingTimeline] = useState(true);
    const [notification, setNotification] = useState({ message: '', type: '', visible: false });
    const notificationTimeoutRef = useRef(null);

    useEffect(() => {
        if (currentUsername !== 'User') {
            fetchMediaStats();
        }
        fetchGameSessions();
    }, [currentUsername]);

    // Cleanup notification timeout on unmount
    useEffect(() => {
        return () => {
            if (notificationTimeoutRef.current) {
                clearTimeout(notificationTimeoutRef.current);
            }
        };
    }, []);

    const showNotification = (message, type = 'info') => {
        // Clear previous timeout if exists
        if (notificationTimeoutRef.current) {
            clearTimeout(notificationTimeoutRef.current);
        }
        
        setNotification({ message, type, visible: true });
        notificationTimeoutRef.current = setTimeout(() => {
            setNotification({ message: '', type: '', visible: false });
            notificationTimeoutRef.current = null;
        }, 3000);
    };

    const renderNotification = () => {
        if (!notification.visible) return null;

        const bgColor = {
            'success': 'bg-green-500',
            'error': 'bg-red-500',
            'info': 'bg-blue-500'
        }[notification.type] || 'bg-blue-500';

        return (
            <div className={`fixed bottom-4 right-4 ${bgColor} text-white px-6 py-3 rounded-lg shadow-lg z-40 max-w-md`}>
                {notification.message}
            </div>
        );
    };

    const fetchMediaStats = async () => {
        try {
            setLoadingStats(true);
            const response = await fetch(`${apiBasePath}/media_aws`);
            const mediaData = await response.json();

            const stats = mediaData.reduce((acc, item) => {
                if (item.type === 'screenshot') acc.screenshots++;
                if (item.type === 'video') acc.videos++;
                if (item.type === 'audio') acc.audio++;
                return acc;
            }, { screenshots: 0, videos: 0, audio: 0 });

            setMediaStats(stats);
        } catch (error) {
            console.error('Error fetching media stats:', error);
        } finally {
            setLoadingStats(false);
        }
    };

    const fetchGameSessions = async () => {
        try {
            setLoadingTimeline(true);
            const response = await fetch(`${apiBasePath}/sessions/list`);
            const sessions = await response.json();

            // Format sessions for timeline display
            const timeline = sessions.map((session, index) => {
                const startDate = new Date(session.start_timestamp);
                const userDisplay = session.user_with === '0' || !session.user_with ? 'myself' : session.user_with;
                return {
                    id: index,
                    title: `Played ${session.app_name || 'Session'} with ${userDisplay}`,
                    date: startDate.toLocaleDateString(),
                    timestamp: startDate,
                    app_name: session.app_name,
                    user_with: session.user_with,
                    status: session.status,
                    start_timestamp: session.start_timestamp,
                    end_timestamp: session.end_timestamp
                };
            })
            // Sort by start_timestamp descending (newest first)
            .sort((a, b) => b.timestamp - a.timestamp);

            setGameEvents(timeline);
        } catch (error) {
            console.error('Error fetching game sessions:', error);
        } finally {
            setLoadingTimeline(false);
        }
    };

    const handleDeleteSuccess = (timestamp) => {
        const updatedEvents = gameEvents.filter(e => e.start_timestamp !== timestamp);
        setGameEvents(updatedEvents);
    };

    const renderStatsSummary = () => {
        if (loadingStats) {
            return (
                <div className="animate-pulse bg-white rounded-lg border border-gray-200 p-6 mb-8">
                    <div className="h-4 bg-gray-200 rounded w-1/4 mb-4"></div>
                    <div className="grid grid-cols-3 gap-4">
                        <div className="h-16 bg-gray-200 rounded"></div>
                        <div className="h-16 bg-gray-200 rounded"></div>
                        <div className="h-16 bg-gray-200 rounded"></div>
                    </div>
                </div>
            );
        }

        return (
            <div className="bg-white rounded-lg border border-gray-200 p-6 mb-8">
                <div className="mb-4">
                    <h2 className="text-xl font-semibold text-gray-700">Media Statistics for {currentUsername}</h2>
                </div>
                <div className="grid grid-cols-3 gap-6">
                    <div className="bg-blue-50 rounded-lg p-4 text-center">
                        <div className="text-2xl font-bold text-blue-600 mb-1">{mediaStats.screenshots}</div>
                        <div className="text-sm text-gray-600">Screenshots</div>
                    </div>
                    <div className="bg-green-50 rounded-lg p-4 text-center">
                        <div className="text-2xl font-bold text-green-600 mb-1">{mediaStats.videos}</div>
                        <div className="text-sm text-gray-600">Videos</div>
                    </div>
                    <div className="bg-purple-50 rounded-lg p-4 text-center">
                        <div className="text-2xl font-bold text-purple-600 mb-1">{mediaStats.audio}</div>
                        <div className="text-sm text-gray-600">Audio</div>
                    </div>
                </div>
            </div>
        );
    };

    return (
        <div className="flex-1 p-8 overflow-y-auto">
            <header className="flex justify-between items-center mb-6">
                <h1 className="text-2xl font-semibold text-gray-700">Statistics</h1>
            </header>

            {renderStatsSummary()}

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
                    <Timeline 
                        events={gameEvents} 
                        apiBasePath={apiBasePath}
                        onNotification={showNotification}
                        onDeleteSuccess={handleDeleteSuccess}
                    />
                )}
            </div>

            {renderNotification()}
        </div>
    );
}

export default StatsPage;