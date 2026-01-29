const os = window.require('os');
const path = window.require('path');
const fs = window.require('fs');
const { spawn, spawnSync } = window.require('child_process');
const { ipcRenderer } = window.require('electron');

const isDev = process.env.NODE_ENV === 'development' || !app.isPackaged;

/**
 * Everything below here up to the class is related to platform detection and
 * setting up paths for FFMpeg binaries
 */

let raw_platform = os.platform();
if (raw_platform === 'darwin') {
    raw_platform = 'mac';
} else if (raw_platform === 'win32') {
    raw_platform = 'win';
}
const platform = raw_platform;

if (platform === 'linux' && platform !== 'mac' && platform !== 'win' && platform !== "browser") {
    console.error('Unsupported platform: ', platform);
    process.exit(1)
}

const arch = os.arch();
if (platform === 'mac' && (arch !== 'x64' && arch !== 'arm64')) {
    console.error('Unsupported architecture: ', arch)
    process.exit(1)
}

const rootPath = ipcRenderer.sendSync('get-root-path');

const ffmpegDir = path.join(
    rootPath,
    'bin',
    platform,
    arch
);

const defaultFFMpegPath = path.join(
    ffmpegDir,
    platform === 'win' ? 'ffmpeg.exe' : 'ffmpeg'
);

// Download FFMpeg binary if it is not there (only in dev mode)
// Just do this for the overlay tool to avoid complications with the main app
if (isDev && window.location.href.includes('overlay')) {
    if ((platform === 'win' || platform === 'mac') && arch === 'x64') {
        const ffmpegExists = fs.existsSync(defaultFFMpegPath);
        if (!ffmpegExists) {
            console.log('FFMpeg binary not found, downloading...');
            console.log('This may take a few minutes depending on your internet speed.');
            let output;
            if (platform === 'win') {
                output = spawnSync(
                    'powershell', 
                    ['-File', path.join(rootPath, 'bin', 'install_win64.ps1')], 
                    { stdio: ['ignore', 'pipe', 'pipe'] }
                );
            } else if (platform === 'mac') {
                output = spawnSync(
                    'bash', 
                    [path.join(rootPath, 'bin', 'install_mac64.sh')],
                    { stdio: ['ignore', 'pipe', 'pipe'] }
                );
            }
            console.log(output.stdout.toString());
            console.log('FFMpeg download script exited with code:', output.status);
        }
    }
}

const VERBOSE = true;

/**
 * FFMpeg class to handle screenshot, video recording, and audio recording.
 * This class is a singleton and should be imported directly.
 */
class FFMpeg {
    constructor(
        ffmpegPath = defaultFFMpegPath, 
        screenshotPath = null, 
        audioRecordingPath = null, 
        videoRecordingPath = null, 
        thumbnailPath = null
    ) {
        this.path = ffmpegPath;
        this.screenshotPath = screenshotPath || path.join(
            rootPath,
            '../screenshots'
        );
        this.audioRecordingPath = audioRecordingPath || path.join(
            rootPath,
            '../audio'
        );
        this.videoRecordingPath = videoRecordingPath || path.join(
            rootPath,
            '../recordings'
        );
        this.thumbnailPath = thumbnailPath || path.join(
            rootPath,
            '../recordings',
            'thumbnails'
        );
        this.process = null;
        this.currentRecordingName = null;
    }

    /**
     * Takes a screenshot and saves it to the specified path.
     * @returns {Promise<File>} The screenshot file.
     */
    async takeScreenshot() {
        return new Promise((resolve, reject) => {
            const screenshotName = `screenshot_${Date.now()}.png`;
            const screenshotPath = path.join(
                this.screenshotPath,
                screenshotName
            );
            const process = spawn(
                this.path,
                [...this.getScreenshotArgs(), screenshotPath],
                { stdio: ['ignore', 'ignore', 'pipe'] }
            );
            process.on('exit', (code) => {
                if (code === 0) {
                    // Return File object of the screenshot
                    const screenshot = new File(
                        [fs.readFileSync(screenshotPath)],
                        screenshotName,
                    );
                    resolve(screenshot);
                } else {
                    reject(new Error(`FFMpeg screenshot process exited with code ${code}`));
                }
            });
            process.stderr.on('data', (data) => {
                if (VERBOSE)
                    console.log(`FFMpeg stderr: ${data}`);
            });
        });
    }

    /**
     * Starts video recording with optional audio.
     * @param {boolean} withAudio - Whether to record audio.
     * @param {string|null} audioDevice - The audio device to use.
     * @returns {Promise<void>} Resolves when recording starts.
     */
    async startVideoRecording(withAudio = false, audioDevice = null) {
        if (VERBOSE)
            console.log('Starting FFMpeg at path:', this.path);

        return new Promise((resolve, reject) => {
            if (this.process) {
                reject(new Error('FFMpeg is already running a process'));
                return;
            }
            // Spawn FFMpeg process to record the screen
            this.currentRecordingName = `recording_${Date.now()}`;
            const args = [...this.getVideoRecordingArgs()];
            if (withAudio) {
                args.push(...this.getAudioRecordingArgs(audioDevice), '-acodec', 'aac', '-strict' , 'experimental');
            }
            // args.push('-c:v', 'libx264', '-crf', '28', '-preset', 'veryfast');
            this.process = spawn(
                this.path, 
                [...args, path.join(this.videoRecordingPath, this.currentRecordingName + '.mkv')], 
                {stdio: ['pipe', 'pipe', 'pipe']}
            );

            let opened = false;

            this.process.on('spawn', () => {
                console.log('FFMpeg process started');
                setTimeout(() => {
                    if (!opened) {
                        this.process.kill('SIGKILL');
                        this.process = null;
                        reject(new Error('FFMpeg failed to start recording in time'));
                    }
                }, 5000);
            });

            this.process.on('error', (err) => {
                this.process = null;
                reject(new Error(`Failed to start FFMpeg: ${err.message}`));
            });

            this.process.stderr.on('data', (data) => {
                if (VERBOSE)
                    console.log(`FFMpeg stderr: ${data}`);
                // Resolve when we see the first frame being recorded
                if (data.toString().includes('frame=')) {
                    opened = true;
                    resolve();
                }
            });
        });
    }

    /**
     * Stops the current video recording.
     * @returns {Promise<void>} Resolves when recording stops.
     */
    async stopVideoRecording() {
        return new Promise((resolve, reject) => {
            if (this.process) {
                // Set a timeout to force kill if not exiting in time
                const timeout = setTimeout(() => {
                    if (this.process) {
                        // Force killing will corrupt the video, but ensures process termination
                        if (VERBOSE)
                            console.log('Force killing FFMpeg process');
                        this.process.kill('SIGKILL');
                        this.process = null;
                        reject(new Error('FFMpeg process force killed due to timeout'));
                    }
                }, 5000);

                // Only resolve when process exits
                // We also need to generate the thumbnail after recording stops
                this.process.on('exit', (code) => {
                    if (VERBOSE)
                        console.log(`FFMpeg process exited with code ${code}`);
                    this.process = null;
                    clearTimeout(timeout);

                    // Also generate the video thumbnail
                    const thumbnailPath = path.join(
                        this.thumbnailPath,
                        this.currentRecordingName + '.png'
                    );
                    // Spawn FFMpeg process to generate thumbnail
                    // -i : input file (last recorded video)
                    // -ss : seek to 1 second
                    // -vframes 1 : capture 1 frame
                    // thumbnailPath : output file
                    this.process = spawn(this.path, [
                        '-i', path.join(this.videoRecordingPath, this.currentRecordingName + '.mp4'),
                        '-ss', '00:00:01.000',
                        '-vframes', '1',
                        thumbnailPath
                    ], { stdio: ['ignore', 'ignore', 'ignore'] });

                    this.process.on('exit', (code) => {
                        if (VERBOSE)
                            console.log(`Thumbnail generation exited with code ${code}`);
                        this.process = null;
                    });

                    resolve();
                });

                // Send 'q' to gracefully stop recording
                this.process.stdin.write('q\n');
            } else {
                reject(new Error('FFMpeg is not recording or process is not available'));
            }
        });
    }

    /**
     * Starts audio recording with the specified device.
     * @param {string|null} device - The audio device to use.
     * @returns {Promise<void>} Resolves when audio recording starts.
     */
    startAudioRecording(device = null) {
        return new Promise((resolve, reject) => {
            if (device === "none") {
                reject(new Error('Audio recording device is set to none'));
                return;
            }
            if (this.process) {
                reject(new Error('FFMpeg is already running a process'));
                return;
            }

            this.currentRecordingName = `audio_recording_${Date.now()}`;
            this.process = spawn(
                this.path, 
                [...this.getAudioRecordingArgs(device), path.join(this.audioRecordingPath, this.currentRecordingName + '.mp3')], 
                {stdio: ['pipe', 'pipe', 'pipe']}
            );

            this.process.on('spawn', () => {
                if (VERBOSE)
                    console.log('FFMpeg audio recording process started');
                resolve();
            });

            this.process.on('error', (err) => {
                this.process = null;
                reject(new Error(`Failed to start FFMpeg audio recording: ${err.message}`));
            });

            this.process.stderr.on('data', (data) => {
                if (VERBOSE)
                    console.log(`FFMpeg stderr: ${data}`);
            });
        });
    }

    /**
     * Stops the current audio recording.
     * @returns {Promise<void>} Resolves when audio recording stops.
     */
    stopAudioRecording() {
        return new Promise((resolve, reject) => {
            if (this.process) {
                // Set a timeout to force kill if not exiting in time
                const timeout = setTimeout(() => {
                    if (this.process) {
                        // Force killing will corrupt the video, but ensures process termination
                        if (VERBOSE)
                            console.log('Force killing FFMpeg process');
                        this.process.kill('SIGKILL');
                        this.process = null;
                        reject(new Error('FFMpeg process force killed due to timeout'));
                    }
                }, 5000);

                // Only resolve when process exits
                this.process.on('exit', (code) => {
                    if (VERBOSE)
                        console.log(`FFMpeg audio recording process exited with code ${code}`);
                    this.process = null;
                    clearTimeout(timeout);
                    resolve();
                });

                // Send 'q' to gracefully stop recording
                this.process.stdin.write('q\n');
            } else {
                reject(new Error('FFMpeg audio recording process is not available'));
            }
        });
    }

    /**
     * Gets the arguments for taking a screenshot based on the platform.
     * @returns {string[]} The arguments for the screenshot command.
     */
    getScreenshotArgs() {
        const args = ['-hide_banner', '-y', '-vframes', '1'];
        switch (platform) {
            case 'win':
                // Put new args at the front of existing args to avoid vframes conflict
                args.unshift('-f', 'gdigrab', '-i', 'desktop');
                break;
            default:
                console.error('Screenshot not implemented for this platform:', platform);
        }
        return args;
    }

    /**
     * Gets the arguments for video recording based on the platform.
     * @returns {string[]} The arguments for the video recording command.
     */
    getVideoRecordingArgs() {
        const args = ['-hide_banner'];
        switch (platform) {
            case 'win':
                // Use GDI grab for screen capture
                args.push('-f', 'gdigrab', '-i', 'desktop');
                break;
            case 'mac':
                // DEBUG INFO: Print out Apple devices
                const process = spawn(this.path, ['-f', 'avfoundation', '-list_devices', 'true', '-i', '""'], { stdio: ['ignore', 'pipe', 'pipe'] });
                process.stderr.on('data', (data) => {
                    if (VERBOSE)
                        console.log(`FFMpeg device list: ${data}`);
                });
                console.error("Mac device listing not fully implemented");
                args.push('-f', 'avfoundation', '-i', '1:none');
                break;
            case 'linux':
                // Use X11 screen capture and ALSA for audio
                // Note: This assumes display :0.0 and default audio device hw:0
                args.push('-f', 'x11grab', '-i', ':0.0', '-f', 'alsa', '-ac', '2', '-i', 'hw:0');
                break;
        }
        return args;
    }

    /**
     * Gets the arguments for audio recording based on the specified device.
     * @param {string|null} audioDeviceName - The name of the audio device.
     * @returns {string[]} The arguments for the audio recording command.
     */
    getAudioRecordingArgs(audioDeviceName = null) {
        const args = ['-hide_banner'];
        switch (platform) {
            case 'win':
                if (!audioDeviceName) {
                    // First we need to list audio devices to find the correct one
                    const ffmpegResult = spawnSync(
                        this.path, 
                        ['-list_devices', 'true', '-f', 'dshow', '-i', 'dummy'], 
                        { stdio: ['ignore', 'pipe', 'pipe'] }
                    );
                    const stderrLines = ffmpegResult.stderr.toString().split('\n');
                    const audioDeviceLine = stderrLines.find(line => line.includes('(audio)'));
                    // returns something like 
                    // [dshow @ 000001794310f560] "Microphone Array (Qualcomm(R) Aqstic(TM) ACX Static Endpoints Audio Device)" (audio)
                    audioDeviceName = audioDeviceLine ? audioDeviceLine.split('"')[1] : null;
                    // just get Microphone Array (Qualcomm(R) Aqstic(TM) ACX Static Endpoints Audio Device)
                    if (!audioDeviceName) {
                        throw new Error('No audio recording device found');
                    }
                }
                args.push('-f', 'dshow', '-i', `audio=${audioDeviceName}`);
                break;
            case 'mac':
                args.push('-f', 'avfoundation', '-i', 'none:0');
                break;
            case 'linux':
                args.push('-f', 'alsa', '-ac', '2', '-i', 'hw:0');
                break;
        }
        return args;
    }

    /**
     * Gets the list of available audio and video devices.
     * @returns {Promise<Array<{name: string, type: string}>>} A promise that resolves to the list of devices.
     */
    getDevices() {
        return new Promise((resolve, reject) => {
            switch (platform) {
                case 'win':
                    const ffmpegWin = spawnSync(
                        this.path, 
                        ['-hide_banner', '-list_devices', 'true', '-f', 'dshow', '-i', 'dummy'], 
                        { stdio: ['ignore', 'pipe', 'pipe'] }
                    );
                    const stderrLines = ffmpegWin.stderr.toString().split('\n');
                    const deviceLines = stderrLines.filter(line => line.includes('(audio)') || line.includes('(video)'));
                    const devices = [];
                    const deviceList = deviceLines.forEach(element => {
                        const name = element.split('"')[1];
                        const type = element.includes('(audio)') ? 'audio' : 'video';
                        devices.push({ name, type });
                    });
                    resolve(devices);
                    break;
                case 'mac':
                    const ffmpegResult = spawnSync(
                        this.path,
                        ['-hide_banner', '-f', 'avfoundation', '-list_devices', 'true', '-i', 'dummy'],
                        { stdio: ['ignore', 'pipe', 'pipe'] }
                    );
                    // I don't have access to a Mac to see what this looks like
                    console.error('Device listing for Mac is not implemented yet');
                    if (VERBOSE) 
                        console.log(`FFMpeg device list: ${ffmpegResult.stderr.toString()}`);
                    break;
                case 'linux':
                    // Linux is complicated and I'm also not sure how to list devices for it
                    console.error('Device listing for Linux is not implemented yet');
                    break;
            }
        });
    }
}

export default new FFMpeg();