import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Home, Gamepad2, FolderOpen, Edit, BarChart2 } from 'lucide-react';
import ProfilePicture from './ProfilePicture';
const { ipcRenderer } = window.require('electron');

function Sidebar() {
    const location = useLocation();
    
    const isActive = (path) => {
        return location.pathname === path;
    };

    return (
        <div className="min-w-64 bg-white border-r border-teal-500 text-gray-700 flex flex-col h-full">
            {/* User profile */}
            <ProfilePicture />

            {/* Navigation links */}
            <nav className="flex-grow">
                <Link
                    to="/"
                    className={`flex items-center px-6 py-4 ${
                        isActive('/') ? 'bg-teal-500 text-white' : 'text-teal-500 hover:bg-gray-100'
                    }`}
                >
                    <Home size={20} className="mr-3" />
                    Home
                </Link>
                <Link
                    to="/games"
                    className={`flex items-center px-6 py-4 ${
                        isActive('/games') ? 'bg-teal-500 text-white' : 'text-teal-500 hover:bg-gray-100'
                    }`}
                >
                    <Gamepad2 size={20} className="mr-3" />
                    Apps
                </Link>
                <Link
                    to="/files"
                    className={`flex items-center px-6 py-4 ${
                        isActive('/files') ? 'bg-teal-500 text-white' : 'text-teal-500 hover:bg-gray-100'
                    }`}
                >
                    <FolderOpen size={20} className="mr-3" />
                    Files
                </Link>
                <Link
                    to="/stats"
                    className={`flex items-center px-6 py-4 ${
                        isActive('/stats') ? 'bg-teal-500 text-white' : 'text-teal-500 hover:bg-gray-100'
                    }`}
                >
                    <BarChart2 size={20} className="mr-3" />
                    Statistics
                </Link>
            </nav>

            {/* Bottom links */}
            <div className="p-6 mt-auto">
                <Link
                    to="/settings"
                    className="block text-gray-600 mb-4"
                >
                    Settings
                </Link>
                <button
                    onClick={() => ipcRenderer.send('app-quit')}
                    className="block text-gray-600"
                >
                    Quit
                </button>
            </div>
        </div>
    );
}

export default Sidebar;