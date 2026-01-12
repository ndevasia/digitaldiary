const os = window.require('os');
const path = window.require('path');
const fs = window.require('fs');
const { spawn } = window.require('child_process');
const { ipcRenderer } = window.require('electron');

let platform = os.platform();
if (platform === 'darwin') {
    platform = 'mac';
} else if (platform === 'win32') {
    platform = 'win';
}

if (platform === 'linux' && platform !== 'mac' && platform !== 'win' && platform !== "browser") {
    console.error('Unsupported platform: ', platform);
    process.exit(1)
}

const arch = os.arch();
if (platform === 'mac' && (arch !== 'x64' &&  arch !== 'arm64')) {
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

export class FFMpeg {
    constructor(ffmpegPath = defaultFFMpegPath, recordingPath = null, thumbnailPath = null) {
        this.path = ffmpegPath;
        this.recordingPath = recordingPath || path.join(
            rootPath,
            '../recordings'
        );
        this.thumbnailPath = thumbnailPath || path.join(
            rootPath,
            '../recordings',
            'thumbnails'
        );
        this.isRecording = false;
        this.process = null;
        this.currentVideoName = null;
    }

    async startVideoRecording() {
        console.log('Starting FFMpeg at path:', this.path);

        return new Promise((resolve, reject) => {
            // Spawn FFMpeg process to record the screen
            this.currentVideoName = `recording_${Date.now()}`;
            this.process = spawn(this.path, ['-filter_complex', 'ddagrab=0,hwdownload,format=bgra', '-c:v', 'libx264', '-crf', '20', path.join(this.recordingPath, this.currentVideoName + '.mp4')], {
                stdio: ['pipe', 'pipe', 'pipe']
            });

            this.process.on('spawn', () => {
                console.log('FFMpeg process started');
                this.isRecording = true;
                resolve();
            });

            this.process.on('error', (err) => {
                this.isRecording = false;
                this.process = null;
                reject(new Error(`Failed to start FFMpeg: ${err.message}`));
            });

            this.process.stderr.on('data', (data) => {
                console.log(`FFMpeg stderr: ${data}`);
            });
        });
    }

    async stopVideoRecording() {
        return new Promise((resolve, reject) => {
            if (this.isRecording && this.process) {
                this.process.on('exit', (code) => {
                    console.log(`FFMpeg process exited with code ${code}`);
                    this.isRecording = false;
                    this.process = null;

                    // Also generate the video thumbnail
                    const thumbnailPath = path.join(
                        this.thumbnailPath,
                        this.currentVideoName + '.png'
                    );
                    // Spawn FFMpeg process to generate thumbnail
                    // -i : input file (last recorded video)
                    // -ss : seek to 1 second
                    // -vframes 1 : capture 1 frame
                    // thumbnailPath : output file
                    this.process = spawn(this.path, [
                        '-i', path.join(this.recordingPath, this.currentVideoName + '.mp4'), 
                        '-ss', '00:00:01.000', 
                        '-vframes', '1', 
                        thumbnailPath
                    ], { stdio: ['ignore', 'ignore', 'ignore'] });

                    this.process.on('exit', (code) => {
                        console.log(`Thumbnail generation exited with code ${code}`);
                        this.process = null;
                    });

                    resolve();
                });

                // Send 'q' to gracefully stop recording
                this.process.stdin.write('q\n');

                setTimeout(() => {
                    if (this.isRecording) {
                        // Force killing will corrupt the video, but ensures process termination
                        console.log('Force killing FFMpeg process');
                        this.process.kill('SIGKILL');
                        reject(new Error('FFMpeg process force killed due to timeout'));
                    }
                }, 5000);
            } else {
                reject(new Error('FFMpeg is not recording or process is not available'));
            }
        });
    }
}