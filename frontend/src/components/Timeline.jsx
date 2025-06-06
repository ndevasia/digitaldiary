import React from 'react';
import { Gamepad2 } from 'lucide-react';

function Timeline({ events }) {
    return (
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
                                    <span className="text-gray-600">Played {event.title}</span>
                                    <span className="text-sm text-gray-500">{event.date}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Timeline;