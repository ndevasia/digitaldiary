import React, { useState, useRef } from 'react';
import { Gamepad2, Trash2 } from 'lucide-react';

function Timeline({ events, onDeleteEvent, apiBasePath, onNotification, onDeleteSuccess }) {
    const [deleteConfirmation, setDeleteConfirmation] = useState({ visible: false, event: null });
    const notificationTimeoutRef = useRef(null);

    const handleDeleteClick = (event) => {
        const userDisplay = event.user_with === '0' || !event.user_with ? 'myself' : event.user_with;
        setDeleteConfirmation({ visible: true, event, userDisplay });

        // Also call the parent's onDeleteEvent if provided (for external handlers)
        if (onDeleteEvent) {
            onDeleteEvent(event);
        }
    };

    const handleConfirmDelete = async () => {
        if (!apiBasePath || !onNotification) {
            console.error('apiBasePath and onNotification are required for delete functionality');
            setDeleteConfirmation({ visible: false, event: null });
            return;
        }

        setDeleteConfirmation({ visible: false, event: null });

        try {
            const response = await fetch(`${apiBasePath}/session/delete`, {
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

            // Call the success callback to update parent's event list
            if (onDeleteSuccess) {
                onDeleteSuccess(deleteConfirmation.event.start_timestamp);
            }

            onNotification('Session deleted', 'success');
        } catch (error) {
            console.error('Error deleting session:', error);
            onNotification('Error: ' + error.message, 'error');
        }
    };

    const handleCancel = () => {
        setDeleteConfirmation({ visible: false, event: null });
    };

    const renderDeleteConfirmationModal = () => {
        if (!deleteConfirmation.visible) return null;

        const message = `Delete session "${deleteConfirmation.event?.app_name}" with ${deleteConfirmation.userDisplay}?`;

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
                        <h2 className="text-xl font-semibold">Delete Session</h2>
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
                                onClick={handleConfirmDelete}
                                className="px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-lg transition-colors"
                            >
                                Delete
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        );
    };
    return (
        <>
            <div className="w-full max-w-4xl mx-auto p-6">
                <div className="relative">
                    {/* Vertical line */}
                    <div className="absolute left-4 top-0 bottom-0 w-0.5 bg-teal-200"></div>

                    {/* Timeline items */}
                    {events.map((event, index) => (
                        <div key={index} className="relative mb-8 last:mb-0">
                            {/* Dot */}
                            <div className="absolute left-0 w-8 h-8 rounded-full bg-teal-500 border-4 border-white flex items-center justify-center">
                                <Gamepad2 size={14} className="text-white" />
                            </div>

                            {/* Content */}
                            <div className="ml-12">
                                <div className="bg-white rounded-lg shadow-sm border border-teal-100 p-4">
                                    <div className="flex items-center justify-between">
                                        <span className="text-gray-600"> {event.title}</span>
                                        <div className="flex items-center gap-2">
                                            <span className="text-sm text-gray-500">{event.date}</span>
                                            {apiBasePath && onNotification && (
                                                <button
                                                    onClick={() => handleDeleteClick(event)}
                                                    className="text-red-500 hover:text-red-700 hover:bg-red-50 p-1 rounded transition-colors"
                                                    title="Delete event"
                                                >
                                                    <Trash2 size={16} />
                                                </button>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
            
            {renderDeleteConfirmationModal()}
        </>
    );
}

export default Timeline;