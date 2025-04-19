import React, { useState, useEffect, useRef } from 'react';
import { Upload, X, Image } from 'lucide-react';

function HeroImage({ defaultImage, onImageChange }) {
    const [heroImage, setHeroImage] = useState(null);
    const [isUploading, setIsUploading] = useState(false);
    const [showHeroEditOptions, setShowHeroEditOptions] = useState(false);
    const [allScreenshots, setAllScreenshots] = useState([]);
    const [loadingAllScreenshots, setLoadingAllScreenshots] = useState(false);
    const [showScreenshotSelector, setShowScreenshotSelector] = useState(false);
    const fileInputRef = useRef(null);
    
    useEffect(() => {
        // Load hero image from localStorage if it exists, otherwise use default image
        const savedHeroImage = localStorage.getItem('heroImage');
        if (savedHeroImage) {
            setHeroImage(savedHeroImage);
        } else if (defaultImage) {
            setHeroImage(defaultImage);
        }
    }, [defaultImage]);
    
    const fetchAllScreenshots = async () => {
        try {
            console.log('Fetching all screenshots...');
            const response = await fetch('/api/media_aws');
            if (!response.ok) {
                throw new Error('Failed to fetch screenshots');
            }
            const data = await response.json();
            console.log('API Response:', data);

            if (!Array.isArray(data)) {
                console.error('API response is not an array:', data);
                return;
            }

            // Filter for screenshots only
            const screenshots = data.filter(item => item.type === 'screenshot');
            console.log('Filtered screenshots:', screenshots);

            setAllScreenshots(screenshots);
        } catch (error) {
            console.error('Error fetching screenshots:', error);
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
                localStorage.setItem('heroImage', imageDataUrl);
                setIsUploading(false);
                setShowHeroEditOptions(false);
                
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
    
    const removeHeroImage = () => {
        setHeroImage(null);
        localStorage.removeItem('heroImage');
        setShowHeroEditOptions(false);
        
        // Notify parent component about the change
        if (onImageChange) {
            onImageChange(null);
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
    
    const handleScreenshotSelect = (screenshotUrl) => {
        setHeroImage(screenshotUrl);
        localStorage.setItem('heroImage', screenshotUrl);
        setShowScreenshotSelector(false);
        setShowHeroEditOptions(false);
        
        // Notify parent component about the change
        if (onImageChange) {
            onImageChange(screenshotUrl);
        }
    };
    
    return (
        <div className="mb-8">
            <div 
                className="relative h-64 md:h-80 w-full rounded-lg overflow-hidden cursor-pointer"
                onMouseEnter={() => setShowHeroEditOptions(true)}
                onMouseLeave={() => setShowHeroEditOptions(false)}
            >
                {heroImage ? (
                    <>
                        <img 
                            src={heroImage} 
                            alt="Hero" 
                            className="w-full h-full object-cover"
                            onClick={handleHeroImageClick}
                        />
                        
                        {/* Edit options that appear on hover */}
                        {showHeroEditOptions && (
                            <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center gap-4">
                                <button 
                                    onClick={handleSelectFromScreenshots}
                                    className="bg-white text-gray-800 p-2 rounded-full hover:bg-gray-100 transition-all flex items-center gap-2"
                                >
                                    <Image size={20} />
                                    <span>Choose from Screenshots</span>
                                </button>
                                <button 
                                    onClick={triggerFileInput}
                                    className="bg-white text-gray-800 p-2 rounded-full hover:bg-gray-100 transition-all flex items-center gap-2"
                                >
                                    <Upload size={20} />
                                    <span>Upload New</span>
                                </button>
                                <button 
                                    onClick={removeHeroImage}
                                    className="bg-white text-gray-800 p-2 rounded-full hover:bg-gray-100 transition-all flex items-center gap-2"
                                >
                                    <X size={20} />
                                    <span>Remove</span>
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
                        ) : allScreenshots.length > 0 ? (
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                {allScreenshots.map((screenshot, index) => (
                                    <div 
                                        key={index} 
                                        className="bg-gray-50 rounded-lg overflow-hidden cursor-pointer hover:shadow-md transition-all"
                                        onClick={() => handleScreenshotSelect(screenshot.media_url)}
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