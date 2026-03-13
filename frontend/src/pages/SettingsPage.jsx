import FFMpeg from "../FFMpeg";
import { useEffect, useState } from "react"
import Sidebar from "../components/Sidebar";

function SettingsPage() {

    let [audioDevices, setAudioDevices] = useState(null);
    let [selectedAudioDevice, setSelectedAudioDevice] = useState("none");
    let [loadingAudioDevices, setLoadingAudioDevices] = useState(true);
    let [recordAudioWithScreen, setRecordAudioWithScreen] = useState(localStorage.getItem('recordAudioWithScreen') === "true");

    // Fetch audio devices on mount
    useEffect(() => {
        fetchDevices().then(fetchSelectedDevice).finally(() => {
            setLoadingAudioDevices(false);
        });
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
            </section>
        </div>
    );
}

export default SettingsPage;