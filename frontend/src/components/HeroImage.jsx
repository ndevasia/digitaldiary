import React, { useState, useEffect, useRef } from 'react';
import { Upload, X, Image, Camera, Trash2, Settings2, ChevronDown } from 'lucide-react';

function HeroImage({ onImageChange }) {
    const [heroImage, setHeroImage] = useState(null);
    const [isUploading, setIsUploading] = useState(false);
    const [showHeroEditOptions, setShowHeroEditOptions] = useState(false);
    const [allScreenshots, setAllScreenshots] = useState([]);
    const [loadingAllScreenshots, setLoadingAllScreenshots] = useState(false);
    const [showScreenshotSelector, setShowScreenshotSelector] = useState(false);
    const [noScreenshotsAvailable, setNoScreenshotsAvailable] = useState(false);
    const [error, setError] = useState(null);
    const [showOptions, setShowOptions] = useState(false);
    const fileInputRef = useRef(null);
    const optionsRef = useRef(null);
    
    useEffect(() => {
        // Fetch both hero image and screenshots when component mounts
        const initializeComponent = async () => {
            await fetchHeroImage();
            await fetchAllScreenshots();
        };
        
        initializeComponent();
    }, []);
    
    useEffect(() => {
        // Close dropdown when clicking outside
        function handleClickOutside(event) {
            if (optionsRef.current && !optionsRef.current.contains(event.target)) {
                setShowOptions(false);
            }
        }

        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, []);
    
    const fetchHeroImage = async () => {
        try {
            setError(null);
            console.log('Fetching hero image from backend...');
            const response = await fetch('/api/user/hero-image');
            if (!response.ok) {
                throw new Error('Failed to fetch hero image');
            }
            const data = await response.json();
            console.log('Hero image API response:', data);
            
            if (data.hero_image_url) {
                console.log('Setting hero image from backend:', data.hero_image_url);
                setHeroImage(data.hero_image_url);
                setNoScreenshotsAvailable(false);
                
                // Notify parent component about the change
                if (onImageChange) {
                    onImageChange(data.hero_image_url);
                }
            } else {
                console.log('No hero image returned from backend');
                setNoScreenshotsAvailable(true);
            }
        } catch (error) {
            console.error('Error fetching hero image:', error);
            setError('Failed to load hero image. Please try again later.');
            setNoScreenshotsAvailable(true);
        }
    };
    
    const fetchAllScreenshots = async () => {
        try {
            setError(null);
            setLoadingAllScreenshots(true);
            console.log('Fetching all screenshots...');
            const response = await fetch('/api/media_aws');
            if (!response.ok) {
                throw new Error('Failed to fetch screenshots');
            }
            const data = await response.json();
            console.log('API Response:', data);

            if (!Array.isArray(data)) {
                throw new Error('Invalid response format from server');
            }

            // Filter for screenshots only and sort by timestamp (newest first)
            const screenshots = data
                .filter(item => item.type === 'screenshot')
                .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
                
            console.log('Filtered screenshots:', screenshots);
            setAllScreenshots(screenshots);
            setNoScreenshotsAvailable(screenshots.length === 0);
        } catch (error) {
            console.error('Error fetching screenshots:', error);
            setError('Failed to load screenshots. Please try again later.');
            setNoScreenshotsAvailable(true);
        } finally {
            setLoadingAllScreenshots(false);
        }
    };
    
    const handleFileUpload = async (event) => {
        const file = event.target.files[0];
        if (file) {
            try {
                setError(null);
                setIsUploading(true);
                
                // Create a FileReader to read the file as a data URL
                const reader = new FileReader();
                
                reader.onload = async (e) => {
                    const imageDataUrl = e.target.result;
                    
                    // Update the backend with the new image URL
                    try {
                        const response = await fetch('/api/user/hero-image', {
                            method: 'PUT',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({
                                image_url: imageDataUrl
                            })
                        });

                        if (!response.ok) {
                            throw new Error('Failed to update hero image');
                        }

                        const data = await response.json();
                        setHeroImage(data.hero_image_url);
                        setShowHeroEditOptions(false);
                        setNoScreenshotsAvailable(false);
                        
                        // Notify parent component about the change
                        if (onImageChange) {
                            onImageChange(data.hero_image_url);
                        }
                    } catch (error) {
                        console.error('Error updating hero image:', error);
                        setError('Failed to update hero image. Please try again.');
                    }
                };
                
                reader.onerror = () => {
                    setError('Failed to read the selected file. Please try again.');
                };
                
                reader.readAsDataURL(file);
            } catch (error) {
                console.error('Error handling file upload:', error);
                setError('Failed to upload file. Please try again.');
            } finally {
                setIsUploading(false);
            }
        }
    };
    
    const handleScreenshotSelect = async (screenshot) => {
        try {
            setError(null);
            // Update the default hero image in the backend
            const response = await fetch('/api/user/hero-image', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    image_url: screenshot.media_url
                })
            });

            if (!response.ok) {
                throw new Error('Failed to update hero image');
            }

            const data = await response.json();
            
            // Update the UI
            setHeroImage(data.hero_image_url);
            setShowScreenshotSelector(false);
            setShowHeroEditOptions(false);
            
            // Notify parent component if needed
            if (onImageChange) {
                onImageChange(data.hero_image_url);
            }
        } catch (error) {
            console.error('Error setting default hero image:', error);
            setError('Failed to set selected image as hero image. Please try again.');
        }
    };
    
    const triggerFileInput = () => {
        fileInputRef.current.click();
    };
    
    const handleHeroImageClick = () => {
        setShowHeroEditOptions(true);
    };
    
    const handleSelectFromScreenshots = () => {
        fetchAllScreenshots();
        setShowScreenshotSelector(true);
    };
    
    const handleRemoveHeroImage = async () => {
        try {
            setError(null);
            // Update the backend to remove the hero image
            const response = await fetch('/api/user/hero-image', {
                method: 'DELETE'
            });

            if (!response.ok) {
                throw new Error('Failed to remove hero image');
            }

            // Update the UI
            setHeroImage(null);
            setShowHeroEditOptions(false);
            
            // Notify parent component about the change
            if (onImageChange) {
                onImageChange(null);
            }
        } catch (error) {
            console.error('Error removing hero image:', error);
            setError('Failed to remove hero image. Please try again.');
        }
    };
    
    return (
        <div className="mb-8">
            {error && (
                <div className="mb-4 p-4 bg-red-100 text-red-700 rounded-lg">
                    {error}
                </div>
            )}
            
            {/* Hero Image Section */}
            <div className="relative h-96 md:h-[32rem] w-full rounded-lg overflow-hidden">
                {heroImage ? (
                    <img 
                        src={heroImage} 
                        alt="Hero" 
                        className="w-full h-full object-contain bg-gray-100 rounded-lg"
                    />
                ) : (
                    <div className="w-full h-full bg-gradient-to-r from-blue-100 to-teal-100 flex flex-col items-center justify-center p-8 rounded-lg">
                        <div className="text-center">
                            <Image size={40} className="text-teal-500 mb-2 mx-auto" />
                            <p className="text-gray-800 font-medium text-xl mb-2">Set a Hero Image</p>
                            <p className="text-gray-600">Click the options below to set up your hero image</p>
                        </div>
                    </div>
                )}
            </div>

            {/* Options Dropdown */}
            <div className="mt-4 border-t border-gray-100 pt-4 flex justify-end" ref={optionsRef}>
                <div className="relative">
                    <button 
                        onClick={() => setShowOptions(!showOptions)}
                        className="text-gray-600 text-sm px-3 py-1.5 rounded hover:bg-gray-50 transition-all flex items-center gap-1.5 border border-gray-200"
                    >
                        <Settings2 size={16} />
                        <span>Hero Image Options</span>
                        <ChevronDown size={16} className={`ml-1 transition-transform ${showOptions ? 'rotate-180' : ''}`} />
                    </button>

                    {/* Dropdown Menu */}
                    {showOptions && (
                        <div className="absolute right-0 mt-1 w-48 bg-white rounded-md shadow-lg border border-gray-200 py-1 z-10">
                            <button 
                                onClick={() => {
                                    handleSelectFromScreenshots();
                                    setShowOptions(false);
                                }}
                                className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 flex items-center gap-2"
                            >
                                <Image size={16} />
                                <span>Select from Screenshots</span>
                            </button>
                            <button 
                                onClick={() => {
                                    triggerFileInput();
                                    setShowOptions(false);
                                }}
                                className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 flex items-center gap-2"
                            >
                                <Upload size={16} />
                                <span>Upload Image</span>
                            </button>
                            {heroImage && (
                                <button 
                                    onClick={() => {
                                        handleRemoveHeroImage();
                                        setShowOptions(false);
                                    }}
                                    className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 flex items-center gap-2"
                                >
                                    <Trash2 size={16} />
                                    <span>Remove Image</span>
                                </button>
                            )}
                        </div>
                    )}
                </div>
            </div>

            <input 
                type="file" 
                ref={fileInputRef}
                onChange={handleFileUpload}
                accept="image/*"
                className="hidden"
            />
            
            {/* Screenshot selector modal */}
            {showScreenshotSelector && (
                <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
                    <div className="bg-white rounded-lg max-w-4xl w-full max-h-[80vh] overflow-y-auto p-6">
                        <div className="flex justify-between items-center mb-4">
                            <h3 className="text-xl font-semibold">Select a Screenshot</h3>
                            <button 
                                onClick={() => setShowScreenshotSelector(false)}
                                className="text-gray-500 hover:text-gray-700"
                            >
                                <X size={24} />
                            </button>
                        </div>
                        
                        {loadingAllScreenshots ? (
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                {[1, 2, 3, 4, 5, 6].map((_, index) => (
                                    <div key={index} className="animate-pulse bg-blue-100 h-48 rounded"></div>
                                ))}
                            </div>
                        ) : noScreenshotsAvailable ? (
                            <div className="text-center py-12 px-4">
                                <div className="bg-blue-50 rounded-full w-20 h-20 flex items-center justify-center mx-auto mb-4">
                                    <Camera size={40} className="text-blue-500" />
                                </div>
                                <h3 className="text-xl font-semibold text-gray-800 mb-2">No Screenshots Available</h3>
                                <p className="text-gray-600 mb-6">You haven't taken any screenshots yet. Take a screenshot or upload an image from your computer to get started.</p>
                                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                                    <button 
                                        onClick={() => {
                                            setShowScreenshotSelector(false);
                                            // You could add a function here to trigger screenshot capture
                                            // For example: window.electronAPI.takeScreenshot();
                                        }}
                                        className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 transition-all flex items-center justify-center gap-2"
                                    >
                                        <Camera size={20} />
                                        <span>Take Screenshot</span>
                                    </button>
                                    <button 
                                        onClick={() => {
                                            setShowScreenshotSelector(false);
                                            triggerFileInput();
                                        }}
                                        className="bg-gray-200 text-gray-800 px-6 py-2 rounded-lg hover:bg-gray-300 transition-all flex items-center justify-center gap-2"
                                    >
                                        <Upload size={20} />
                                        <span>Upload Image</span>
                                    </button>
                                </div>
                            </div>
                        ) : allScreenshots.length > 0 ? (
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                {allScreenshots.map((screenshot, index) => (
                                    <div 
                                        key={index} 
                                        className="bg-gray-50 rounded-lg overflow-hidden cursor-pointer hover:shadow-md transition-all"
                                        onClick={() => handleScreenshotSelect(screenshot)}
                                    >
                                        <img 
                                            src={screenshot.media_url} 
                                            alt={`Screenshot ${index + 1}`} 
                                            className="w-full h-48 object-cover"
                                        />
                                        <div className="p-3">
                                            <p className="text-sm text-gray-600">
                                                {new Date(screenshot.timestamp).toLocaleDateString()}
                                            </p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <div className="text-center py-8">
                                <p className="text-gray-500">No screenshots available.</p>
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
}

export default HeroImage;