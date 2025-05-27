import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { Home, Gamepad2, FolderOpen, Edit } from 'lucide-react';
import { useAuth } from '../auth/AuthContext';
const { ipcRenderer } = window.require('electron');

function Sidebar() {
    const location = useLocation();
    const navigate = useNavigate();
    const { signOut } = useAuth();
    
    const isActive = (path) => {
        return location.pathname === path;
    };

    const handleLogout = async () => {
        try {
            const result = await signOut();
            if (result.success) {
                navigate('/login');
            }
        } catch (error) {
            console.error('Logout error:', error);
        }
    };
    
    return (
        <div className="w-64 bg-white border-r border-teal-500 text-gray-700 flex flex-col h-full">
            {/* User profile */}
            <div className="flex flex-col items-center p-6 pb-8">
                <div className="w-32 h-32 bg-blue-100 rounded-full border border-teal-500 mb-6"></div>
            </div>
            
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
                    Games
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
                    to="/journals" 
                    className={`flex items-center px-6 py-4 ${
                        isActive('/journals') ? 'bg-teal-500 text-white' : 'text-teal-500 hover:bg-gray-100'
                    }`}
                >
                    <Edit size={20} className="mr-3" />
                    Journals
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
                    onClick={handleLogout}
                    className="block text-gray-600 mb-4 hover:text-red-500 transition-colors"
                >
                    Logout
                </button>
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