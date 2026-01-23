import FFMpeg from "../FFMpeg";
import { useEffect, useState } from "react"
import Sidebar from "../components/Sidebar";

function SettingsPage() {

    let [audioDevices, setAudioDevices] = useState([]);

    useEffect(() => {
        fetchDevices();
    }, [])

    const fetchDevices = async () => {
        const devices = await FFMpeg.getDevices();
        setAudioDevices(devices.filter(d => d.type === 'audio'));
    }

    const updateDevice = (deviceId) => {
        // TODO
    }

    return (<div className="flex h-screen bg-blue-50">
        <Sidebar />

        <div className="flex-1 p-8 overflow-y-auto">
            <header className="flex justify-between items-center mb-6">
                <h1 className="text-2xl font-semibold text-gray-700">Settings</h1>
            </header>

            <section className="mb-8">
                <h2 className="text-xl font-medium text-gray-700 mb-4">Audio Device</h2>
                <div>
                    <select onChange={e => updateDevice(e.target.value)}>
                        {audioDevices.map(device => (
                            <option key={device.id} value={device.id}>{device.name}</option>
                        ))}
                    </select>
                </div>
            </section>
        </div>
    </div>);
}

export default SettingsPage;