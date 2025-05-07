import React, { useState, useEffect, useRef } from 'react';
import { Upload, X, Image, Camera } from 'lucide-react';

function HeroImage({ onImageChange }) {
    const [heroImage, setHeroImage] = useState(null);
    const [isUploading, setIsUploading] = useState(false);
    const [showHeroEditOptions, setShowHeroEditOptions] = useState(false);
    const [allScreenshots, setAllScreenshots] = useState([]);
    const [loadingAllScreenshots, setLoadingAllScreenshots] = useState(false);
    const [showScreenshotSelector, setShowScreenshotSelector] = useState(false);
    const [noScreenshotsAvailable, setNoScreenshotsAvailable] = useState(false);
    const fileInputRef = useRef(null);
    
    useEffect(() => {
        // Fetch the hero image from the backend
        fetchHeroImage();
    }, []);
    
    const fetchHeroImage = async () => {
        try {
            console.log('Fetching hero image from backend...');
            const response = await fetch('/api/hero-image');
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
            setNoScreenshotsAvailable(true);
        }
    };
    
    const fetchAllScreenshots = async () => {
        try {
            setLoadingAllScreenshots(true);
            console.log('Fetching all screenshots...');
            const response = await fetch('/api/media_aws');
            if (!response.ok) {
                throw new Error('Failed to fetch screenshots');
            }
            const data = await response.json();
            console.log('API Response:', data);

            if (!Array.isArray(data)) {
                console.error('API response is not an array:', data);
                setNoScreenshotsAvailable(true);
                return;
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
            setNoScreenshotsAvailable(true);
        } finally {
            setLoadingAllScreenshots(false);
        }
    };
    
    const handleFileUpload = (event) => {
        const file = event.target.files[0];
        if (file) {
            setIsUploading(true);
            
            // Create a FileReader to read the file as a data URL
            const reader = new FileReader();
            
            reader.onload = (e) => {
                const imageDataUrl = e.target.result;
                setHeroImage(imageDataUrl);
                setIsUploading(false);
                setShowHeroEditOptions(false);
                setNoScreenshotsAvailable(false);
                
                // Notify parent component about the change
                if (onImageChange) {
                    onImageChange(imageDataUrl);
                }
            };
            
            reader.onerror = () => {
                console.error('Error reading file');
                setIsUploading(false);
            };
            
            reader.readAsDataURL(file);
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
    
    const handleScreenshotSelect = (screenshot) => {
        setHeroImage(screenshot.media_url);
        setShowScreenshotSelector(false);
        setShowHeroEditOptions(false);
        setNoScreenshotsAvailable(false);
        
        // Notify parent component about the change
        if (onImageChange) {
            onImageChange(screenshot.media_url);
        }
    };
    
    return (
        <div className="mb-8">
            <div 
                className="relative h-96 md:h-[32rem] w-full rounded-lg overflow-hidden cursor-pointer"
                onMouseEnter={() => setShowHeroEditOptions(true)}
                onMouseLeave={() => setShowHeroEditOptions(false)}
            >
                {heroImage ? (
                    <>
                        <img 
                            src={heroImage} 
                            alt="Hero" 
                            className="w-full h-full object-contain bg-gray-100"
                            onClick={handleHeroImageClick}
                        />
                        
                        {/* Edit options that appear on hover */}
                        {showHeroEditOptions && (
                            <div className="absolute inset-0 bg-black/30 backdrop-blur-sm flex items-center justify-center gap-4">
                                <button 
                                    onClick={handleSelectFromScreenshots}
                                    className="bg-white/90 text-gray-800 px-4 py-2 rounded-lg hover:bg-white transition-all flex items-center gap-2 shadow-sm"
                                >
                                    <Image size={20} />
                                    <span>Choose from Screenshots</span>
                                </button>
                                <button 
                                    onClick={triggerFileInput}
                                    className="bg-white/90 text-gray-800 px-4 py-2 rounded-lg hover:bg-white transition-all flex items-center gap-2 shadow-sm"
                                >
                                    <Upload size={20} />
                                    <span>Upload New</span>
                                </button>
                            </div>
                        )}
                    </>
                ) : (
                    <div 
                        className="w-full h-full bg-gradient-to-r from-blue-100 to-teal-100 flex flex-col items-center justify-center cursor-pointer"
                        onClick={triggerFileInput}
                    >
                        <Upload size={40} className="text-teal-500 mb-2" />
                        <p className="text-gray-600 font-medium">Upload a hero image</p>
                        <p className="text-gray-500 text-sm mt-1">Click to select from your computer</p>
                    </div>
                )}
                <input 
                    type="file" 
                    ref={fileInputRef}
                    onChange={handleFileUpload}
                    accept="image/*"
                    className="hidden"
                />
            </div>
            
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