import React from 'react';
import { Link, useLocation } from 'react-router-dom';
const { ipcRenderer } = window.require('electron');

function Sidebar() {
    const location = useLocation();
    
    const isActive = (path) => {
        return location.pathname === path ? 'bg-green-700' : '';
    };
    
    return (
        <div className="w-64 bg-green-600 text-white flex flex-col h-full">
            {/* Avatar placeholder */}
            <div className="flex justify-center my-6">
                <div className="w-24 h-24 bg-green-200 rounded-full"></div>
            </div>
            
            {/* Navigation links */}
            <nav className="flex-grow px-4">
                <ul className="space-y-2">
                    <li>
                        <Link 
                            to="/" 
                            className={`block px-4 py-2 rounded hover:bg-green-700 transition-colors ${isActive('/')}`}
                        >
                            Home
                        </Link>
                    </li>
                    <li>
                        <Link 
                            to="/games" 
                            className={`block px-4 py-2 rounded hover:bg-green-700 transition-colors ${isActive('/games')}`}
                        >
                            Games
                        </Link>
                    </li>
                    <li>
                        <Link 
                            to="/files" 
                            className={`block px-4 py-2 rounded hover:bg-green-700 transition-colors ${isActive('/files')}`}
                        >
                            Files
                        </Link>
                    </li>
                    <li>
                        <Link 
                            to="/journals" 
                            className={`block px-4 py-2 rounded hover:bg-green-700 transition-colors ${isActive('/journals')}`}
                        >
                            Journals
                        </Link>
                    </li>
                </ul>
            </nav>
            
            {/* Bottom links */}
            <div className="p-4 border-t border-green-700">
                <Link to="/settings" className="block py-2 text-center hover:underline">
                    Settings
                </Link>
                <button 
                    onClick={() => ipcRenderer.send('app-quit')} 
                    className="w-full py-2 text-center hover:underline"
                >
                    Quit
                </button>
            </div>
        </div>
    );
}

export default Sidebar;