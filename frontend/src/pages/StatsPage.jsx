import React, { useState, useEffect, useContext } from 'react';
import { BarChart2 } from 'lucide-react';
import Timeline from '../components/Timeline';
import { UserContext } from '../context/UserContext.jsx';

function StatsPage() {
    const user = useContext(UserContext);
    const currentUsername = user?.username || 'User';

    const [mediaStats, setMediaStats] = useState({
        screenshots: 0,
        videos: 0,
        audio: 0
    });
    const [loadingStats, setLoadingStats] = useState(true);
    const [gameEvents, setGameEvents] = useState([]);
    const [loadingTimeline, setLoadingTimeline] = useState(true);

    useEffect(() => {
        if (currentUsername !== 'User') {
            fetchMediaStats();
            fetchGameSessions();
        }
    }, [currentUsername]); 

    const fetchMediaStats = async () => {
        try {
            setLoadingStats(true);
            const response = await fetch(`/api/media_aws?username=${encodeURIComponent(currentUsername)}`);
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
            const response = await fetch(`/api/media_aws?username=${encodeURIComponent(currentUsername)}`);
            const mediaData = await response.json();

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

            const timeline = Object.values(gameSessions)
                .sort((a, b) => b.timestamp - a.timestamp);

            setGameEvents(timeline);
        } catch (error) {
            console.error('Error fetching game sessions:', error);
        } finally {
            setLoadingTimeline(false);
        }
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

export default StatsPage;