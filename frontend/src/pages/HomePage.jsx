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
    const [showSessionModal, setShowSessionModal] = useState(false);
    const [appName, setAppName] = useState('');
    const [userWith, setUserWith] = useState('');
    const [creatingSession, setCreatingSession] = useState(false);
    const [activeSession, setActiveSession] = useState(null);
    const [loadingSession, setLoadingSession] = useState(true);
    const [modalKey, setModalKey] = useState(0);
    const [notification, setNotification] = useState({ message: '', type: '', visible: false });
    const [deleteConfirmation, setDeleteConfirmation] = useState({ visible: false, event: null });
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
        // Fetch active session
        fetchActiveSession();
    }, []);

    // Reset form state whenever modal opens
    useEffect(() => {
        if (showSessionModal) {
            // Increment key to force form remount
            setModalKey(prev => prev + 1);
            // Force a complete reset of form state when modal opens
            setCreatingSession(false);
        }
    }, [showSessionModal]);

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
            const response = await fetch('/api/sessions/list');
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

    const showNotification = (message, type = 'info') => {
        setNotification({ message, type, visible: true });
        setTimeout(() => {
            setNotification({ message: '', type: '', visible: false });
        }, 3000);
    };

    const handleNewMemory = () => {
        // Reset all form and loading state to ensure clean modal opening
        setAppName('');
        setUserWith('');
        setCreatingSession(false);
        setLoadingSession(false);
        setShowSessionModal(true);
    };

    const handleSessionSubmit = async (e) => {
        e.preventDefault();
        
        const trimmedAppName = appName.trim();
        if (!trimmedAppName) {
            showNotification('Please enter an app name', 'error');
            return;
        }

        try {
            setCreatingSession(true);

            // If there's an active session, end it first
            if (activeSession && activeSession.status === 'active') {
                const endResponse = await fetch('/api/session/end', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });

                if (!endResponse.ok) {
                    throw new Error('Failed to end current session');
                }
            }

            // Now create the new session
            const response = await fetch('/api/session/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    appName: trimmedAppName,
                    userWith: userWith.trim()
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || `Server error: ${response.status}`);
            }

            // Update active session state
            setActiveSession({
                app_name: trimmedAppName,
                user_with: userWith.trim(),
                start_timestamp: new Date().toISOString(),
                status: 'active'
            });

            // Clear form fields before closing modal
            setAppName('');
            setUserWith('');
            
            // Close modal
            setShowSessionModal(false);

            // Refresh sessions list
            fetchGameSessions();

            // Show success message
            showNotification('Session started successfully!', 'success');
        } catch (error) {
            console.error('Error creating session:', error);
            showNotification('Error: ' + error.message, 'error');
        } finally {
            setCreatingSession(false);
        }
    };

    const handleCloseSessionModal = () => {
        setAppName('');
        setUserWith('');
        setShowSessionModal(false);
    };

    const handleDeleteTimelineEvent = (event) => {
        const userDisplay = event.user_with === '0' || !event.user_with ? 'myself' : event.user_with;
        setDeleteConfirmation({ visible: true, event, actionType: 'delete', userDisplay });
    };

    const fetchActiveSession = async () => {
        try {
            setLoadingSession(true);
            const response = await fetch('/api/session/latest');
            const data = await response.json();
            
            // Check if session status is active
            if (data.status === 'active') {
                setActiveSession(data);
                // Pre-fill the form with current session data
                setAppName(data.app_name || '');
                setUserWith(data.user_with || '');
            } else {
                setActiveSession(null);
                setAppName('');
                setUserWith('');
            }
        } catch (error) {
            console.error('Error fetching active session:', error);
        } finally {
            setLoadingSession(false);
        }
    };

    const handleEndSession = () => {
        setDeleteConfirmation({ visible: true, event: activeSession, actionType: 'end', userDisplay: '' });
    };

    const handleChangeSession = () => {
        // Reset form state to ensure inputs are fully interactive
        setCreatingSession(false);
        setShowSessionModal(true);
        
        // Pre-fill with current session data
        if (activeSession) {
            setAppName(activeSession.app_name || '');
            setUserWith(activeSession.user_with || '');
        }
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

    // Notification Toast Component
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

    // Confirmation Modal
    const renderConfirmationModal = () => {
        if (!deleteConfirmation.visible) return null;

        const handleConfirm = async () => {
            setDeleteConfirmation({ visible: false, event: null });
            
            if (deleteConfirmation.actionType === 'delete') {
                try {
                    const response = await fetch('/api/session/delete', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            start_timestamp: deleteConfirmation.event.start_timestamp
                        })
                    });

                    if (!response.ok) {
                        const data = await response.json();
                        throw new Error(data.error || 'Failed to delete session');
                    }

                    const updatedEvents = gameEvents.filter(e => e.start_timestamp !== deleteConfirmation.event.start_timestamp);
                    setGameEvents(updatedEvents);
                    showNotification('Session deleted', 'success');
                } catch (error) {
                    console.error('Error deleting session:', error);
                    showNotification('Error: ' + error.message, 'error');
                }
            } else if (deleteConfirmation.actionType === 'end') {
                try {
                    const response = await fetch('/api/session/end', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        }
                    });

                    if (!response.ok) {
                        throw new Error('Failed to end session');
                    }

                    await Promise.all([fetchGameSessions(), fetchActiveSession()]);
                    setShowSessionModal(false);
                    showNotification('Session ended', 'success');
                } catch (error) {
                    console.error('Error ending session:', error);
                    showNotification('Error ending session: ' + error.message, 'error');
                }
            }
        };

        const handleCancel = () => {
            setDeleteConfirmation({ visible: false, event: null });
        };

        const isEndAction = deleteConfirmation.actionType === 'end';
        const title = isEndAction ? 'End Session' : 'Delete Session';
        const message = isEndAction 
            ? 'Are you sure you want to end this session?'
            : `Delete session "${deleteConfirmation.event?.app_name}" with ${deleteConfirmation.userDisplay}?`;

        return (
            <div
                className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
                onClick={handleCancel}
            >
                <div
                    className="bg-white rounded-lg shadow-lg w-full max-w-md mx-4"
                    onClick={(e) => e.stopPropagation()}
                >
                    <div className="bg-red-500 text-white px-6 py-4 rounded-t-lg">
                        <h2 className="text-xl font-semibold">{title}</h2>
                    </div>

                    <div className="px-6 py-6">
                        <p className="text-gray-700 mb-6">{message}</p>
                        <div className="flex gap-3 justify-end">
                            <button
                                onClick={handleCancel}
                                className="px-4 py-2 text-gray-700 bg-gray-200 hover:bg-gray-300 rounded-lg transition-colors"
                            >
                                Cancel
                            </button>
                            <button
                                onClick={handleConfirm}
                                className="px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-lg transition-colors"
                            >
                                {isEndAction ? 'End' : 'Delete'}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        );
    };

    // Session Modal
    const renderSessionModal = () => {
        if (!showSessionModal) return null;

        return (
            <div
                key="session-modal"
                className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
                onClick={(e) => {
                    if (e.currentTarget === e.target) {
                        handleCloseSessionModal();
                    }
                }}
            >
                <div
                    className="bg-white rounded-lg shadow-lg w-full max-w-md mx-4"
                >
                    <div className="bg-teal-500 text-white px-6 py-4 rounded-t-lg flex justify-between items-center">
                        <h2 className="text-xl font-semibold">{activeSession ? 'Change Session' : 'Start New Session'}</h2>
                        <button
                            onClick={handleCloseSessionModal}
                            className="text-white hover:text-gray-200 text-2xl leading-none"
                        >
                            &times;
                        </button>
                    </div>

                    <div className="px-6 py-6">
                        <form key={`form-${modalKey}`} onSubmit={handleSessionSubmit}>
                            <div className="mb-5">
                                <label htmlFor="appName" className="block text-sm font-semibold text-gray-700 mb-2">
                                    What app are you using?
                                </label>
                                <input
                                    type="text"
                                    id="appName"
                                    value={appName}
                                    onChange={(e) => setAppName(e.target.value)}
                                    placeholder="e.g., Discord, Steam, Minecraft"
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
                                    required
                                    autoFocus
                                />
                            </div>

                            <div className="mb-6">
                                <label htmlFor="userWith" className="block text-sm font-semibold text-gray-700 mb-2">
                                    Who are you using it with? <span className="text-gray-500 font-normal">(optional)</span>
                                </label>
                                <input
                                    type="text"
                                    id="userWith"
                                    value={userWith}
                                    onChange={(e) => setUserWith(e.target.value)}
                                    placeholder="Leave empty if using it alone, or enter name/Group"
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
                                />
                            </div>

                            <div className="flex gap-3 justify-end">
                                <button
                                    type="button"
                                    onClick={handleCloseSessionModal}
                                    className="px-4 py-2 text-gray-700 bg-gray-200 hover:bg-gray-300 rounded-lg transition-colors"
                                >
                                    Cancel
                                </button>
                                <button
                                    type="submit"
                                    disabled={creatingSession}
                                    className="px-4 py-2 bg-teal-500 hover:bg-teal-600 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    {creatingSession ? (activeSession ? 'Updating...' : 'Starting...') : (activeSession ? 'Update Session' : 'Start Session')}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        );
    };

    return (
        <div className="flex-1 p-8 overflow-y-auto">
            <header className="flex justify-between items-center mb-6">
                <h1 className="text-2xl font-semibold text-gray-700">Hello, {currentUsername}</h1>
                {activeSession ? (
                    <div className="flex gap-3">
                        <button 
                            onClick={handleChangeSession}
                            className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition-colors text-sm font-medium"
                        >
                            Change Session
                        </button>
                        <button 
                            onClick={handleEndSession}
                            className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg transition-colors text-sm font-medium"
                        >
                            End Session
                        </button>
                    </div>
                ) : (
                    <button 
                        onClick={handleNewMemory}
                        className="bg-teal-500 hover:bg-teal-600 text-white px-6 py-3 rounded-full flex items-center transition-colors"
                    >
                        <Plus size={20} className="mr-2" />
                        Start Session
                    </button>
                )}
            </header>

            {/* Active Session Info */}
            {activeSession && (
                <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                    <h3 className="text-sm font-semibold text-blue-900 mb-2">Active Session</h3>
                    <div className="text-sm text-blue-800">
                        <p><span className="font-medium">App:</span> {activeSession.app_name || 'Not set'}</p>
                        <p><span className="font-medium">With:</span> {activeSession.user_with === '0' || !activeSession.user_with ? 'Myself' : activeSession.user_with}</p>
                    </div>
                </div>
            )}

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

            {/* Session Modal */}
            {renderSessionModal()}

            {/* Confirmation Modal */}
            {renderConfirmationModal()}

            {/* Notification Toast */}
            {renderNotification()}

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
                    <Timeline events={gameEvents} onDeleteEvent={handleDeleteTimelineEvent} />
                )}
            </div>
        </div>
    );
}

export default HomePage;