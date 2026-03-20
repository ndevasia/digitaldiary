import FFMpeg from "../FFMpeg";
import { useEffect, useState } from "react"
import Sidebar from "../components/Sidebar";

function SettingsPage() {

    let [audioDevices, setAudioDevices] = useState(null);
    let [selectedAudioDevice, setSelectedAudioDevice] = useState("none");
    let [loadingAudioDevices, setLoadingAudioDevices] = useState(true);
    let [recordAudioWithScreen, setRecordAudioWithScreen] = useState(localStorage.getItem('recordAudioWithScreen') === "true");
    
    // Friends state
    let [friends, setFriends] = useState([]);
    let [friendUsername, setFriendUsername] = useState("");
    let [addingFriend, setAddingFriend] = useState(false);
    let [friendMessage, setFriendMessage] = useState("");
    let [friendError, setFriendError] = useState("");

    // Fetch audio devices on mount
    useEffect(() => {
        fetchDevices().then(fetchSelectedDevice).finally(() => {
            setLoadingAudioDevices(false);
        });
        fetchFriends();
    }, []);

    // Persist recordAudioWithScreen setting
    useEffect(() => {
        localStorage.setItem('recordAudioWithScreen', recordAudioWithScreen ? "true" : "false");
    }, [recordAudioWithScreen]);

    const fetchSelectedDevice = async () => {
        const storedDevice = localStorage.getItem('audioDeviceName') || "none";
        setSelectedAudioDevice(storedDevice);
    }

    const fetchDevices = async () => {
        const devices = await FFMpeg.getDevices();
        setAudioDevices(devices.filter(d => d.type === 'audio'));
    }

    const updateDevice = (deviceName) => {
        // We use LocalStorage because it's convenient to use and
        // this setting is only needed in the frontend rendering process.
        localStorage.setItem('audioDeviceName', deviceName);
        setSelectedAudioDevice(deviceName);
    }

    const fetchFriends = async () => {
        try {
            const response = await fetch('/api/friends');
            const data = await response.json();
            if (response.ok) {
                setFriends(data.friends || []);
            } else {
                console.error('Error fetching friends:', data.error);
            }
        } catch (error) {
            console.error('Error fetching friends:', error);
        }
    }

    const addFriend = async (e) => {
        e.preventDefault();
        
        if (!friendUsername.trim()) {
            setFriendError("Please enter a username");
            return;
        }

        try {
            setAddingFriend(true);
            setFriendError("");
            setFriendMessage("");

            const response = await fetch('/api/friends/add', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    friend_username: friendUsername.trim()
                })
            });

            const data = await response.json();

            if (!response.ok) {
                setFriendError(data.error || "Failed to add friend");
                return;
            }

            setFriendMessage("Friend added successfully!");
            setFriendUsername("");
            setFriends([...friends, friendUsername.trim()]);
            
            // Clear message after 3 seconds
            setTimeout(() => setFriendMessage(""), 3000);
        } catch (error) {
            console.error('Error adding friend:', error);
            setFriendError("Error adding friend: " + error.message);
        } finally {
            setAddingFriend(false);
        }
    }

    function AudioSelector() {
        if (loadingAudioDevices) {
            return <select disabled value="loading">
                <option key="loading">Loading...</option>
            </select>
        }
        return (
            <select defaultValue={selectedAudioDevice} onChange={e => updateDevice(e.target.value)}>        
                {audioDevices.map(device => (
                    <option 
                        key={device.name} 
                        value={device.name}
                    >{device.name}</option>
                ))}
                <option key="none" value="none">None</option>
            </select>
        );
    }

    return (
        <div className="flex-1 p-8 overflow-y-auto">
            <header className="flex justify-between items-center mb-6">
                <h1 className="text-2xl font-semibold text-gray-700">Settings</h1>
            </header>

            <section className="mb-8 flex flex-col gap-6">
                <div>
                    <h2 className="text-xl font-medium text-gray-700 mb-4">Audio Device</h2>
                    <div>
                        <AudioSelector />
                    </div>
                </div>
                <div>
                    <h2 className="text-xl font-medium text-gray-700 mb-4">Screen Recording</h2>
                    <div className="flex gap-4">
                        <span>Record audio when screen recording </span>
                        <input 
                            type="checkbox" 
                            checked={recordAudioWithScreen} 
                            onChange={e => setRecordAudioWithScreen(e.target.checked)} 
                        />
                    </div>
                </div>
                <div>
                    <h2 className="text-xl font-medium text-gray-700 mb-4">Friends</h2>
                    <div className="flex flex-col gap-4">
                        <form onSubmit={addFriend} className="flex gap-2">
                            <input
                                type="text"
                                placeholder="Enter friend's username"
                                value={friendUsername}
                                onChange={e => setFriendUsername(e.target.value)}
                                className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                disabled={addingFriend}
                            />
                            <button
                                type="submit"
                                disabled={addingFriend}
                                className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 disabled:bg-gray-400 cursor-pointer"
                            >
                                {addingFriend ? "Adding..." : "Add Friend"}
                            </button>
                        </form>
                        {friendError && (
                            <p className="text-red-500 text-sm">{friendError}</p>
                        )}
                        {friendMessage && (
                            <p className="text-green-500 text-sm">{friendMessage}</p>
                        )}
                        {friends.length > 0 && (
                            <div className="mt-4">
                                <h3 className="text-lg font-medium text-gray-700 mb-2">Your Friends</h3>
                                <ul className="space-y-2">
                                    {friends.map(friend => (
                                        <li key={friend} className="text-gray-600 px-3 py-2 bg-gray-100 rounded-md">
                                            {friend}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        )}
                    </div>
                </div>
            </section>
        </div>
    );
}

export default SettingsPage;