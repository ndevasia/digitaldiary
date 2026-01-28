import React, { useState, useRef, useEffect } from 'react';
import { Camera } from 'lucide-react';

const API_BASE_URL = 'http://localhost:5001';

function ProfilePicture() {
    // Initialize as null (we don't know if the user has a pic yet)
    const [profilePic, setProfilePic] = useState(null);
    // New state to track if the image is actually loading successfully
    const [imageLoaded, setImageLoaded] = useState(false);
    const fileInputRef = useRef(null);

    // Fetch the S3 URL when the component first loads
    useEffect(() => {
        fetch(`${API_BASE_URL}/api/profile-pic`)
            .then(res => res.json())
            .then(data => {
                if (data.url) {
                    setProfilePic(data.url);
                    // Don't set imageLoaded true yet, wait for the onLoad event
                }
            })
            .catch(err => console.error("Error fetching profile pic:", err));
    }, []);

    const handleProfilePicClick = () => {
        fileInputRef.current.click();
    };

    const handleFileChange = async (event) => {
        const file = event.target.files[0];
        if (!file) return;

        // Reset load status while uploading
        setImageLoaded(false);

        const formData = new FormData();
        formData.append('file', file);

        try {
            console.log("Uploading...");
            const response = await fetch(`${API_BASE_URL}/api/upload-profile-pic`, {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();

            if (response.ok && data.url) {
                console.log("Upload success, new URL:", data.url);
                // Append a timestamp to force the browser to treat it as a new image
                const timestampedUrl = `${data.url}${data.url.includes('?') ? '&' : '?'}t=${Date.now()}`;
                setProfilePic(timestampedUrl);
            } else {
                console.error("Failed to upload profile picture:", data.error);
            }
        } catch (error) {
            console.error("Error uploading profile picture:", error);
        }
    };

    return (
        <div className="flex flex-col items-center p-6 pb-8">
            <div 
                onClick={handleProfilePicClick}
                className="relative w-32 h-32 bg-blue-100 rounded-full border border-teal-500 mb-6 cursor-pointer overflow-hidden group"
            >
                {/* FIX: We now always render the img tag if a URL exists.
                   We use CSS to hide it until it successfully loads.
                */}
                {profilePic && (
                    <img
                        src={profilePic}
                        alt="Profile"
                        className={`w-full h-full object-cover rounded-full ${imageLoaded ? 'block' : 'hidden'}`}
                        onLoad={() => {
                            console.log("Profile picture loaded successfully!");
                            setImageLoaded(true);
                        }}
                        onError={(e) => { 
                            console.log("Image failed to load (S3 might be slow), hiding it temporarily.");
                            setImageLoaded(false);
                        }}
                    />
                )}

                {/* Placeholder: Only show if we have no URL OR if the image hasn't loaded yet */}
                {(!profilePic || !imageLoaded) && (
                    <div className="absolute inset-0 flex items-center justify-center text-teal-500 font-bold bg-blue-100 rounded-full">
                        User
                    </div>
                )}
                
                {/* Hover Overlay */}
                <div className="absolute inset-0 bg-black bg-opacity-40 flex items-center justify-center opacity-0 group-hover:opacity-60 transition-opacity rounded-full">
                    <Camera className="text-white" size={24} />
                </div>
            </div>

            <input
                type="file"
                accept="image/*"
                ref={fileInputRef}
                onChange={handleFileChange}
                style={{ display: 'none' }}
            />
        </div>
    );
}

export default ProfilePicture;