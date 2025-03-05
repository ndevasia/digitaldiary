const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const isDev = require('electron-is-dev');
const { spawn } = require('child_process');

let mainWindow;
let pythonProcess;

function startPythonBackend() {
    // Path to your Python API server script
    pythonProcess = spawn('python', ['../backend/window/app.py'], {
        stdio: 'inherit'
    });
    
    pythonProcess.on('error', (err) => {
        console.error('Failed to start Python process:', err);
    });
}

function createWindow() {
    const screen = require('electron').screen;
    const display = screen.getPrimaryDisplay();
    const { width } = display.workAreaSize;

    mainWindow = new BrowserWindow({
        width: 800,     // w-16 == 64 Width for icons (16px * 4)
        height: 224,   // h-56 == 224 Height for 3 icons + close button + spacing
        x: width - 100,
        y: 100,
        transparent: true,
        frame: false,
        alwaysOnTop: true,
        resizable: false,
        backgroundColor: '#00ffffff',
        hasShadow: false,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
            enableRemoteModule: true
        }
    });

    // Load the React app
    const startUrl = isDev 
        ? 'http://localhost:5173' // Vite dev server default port
        : `file://${path.join(__dirname, '../dist/index.html')}`;
        
    mainWindow.loadURL(startUrl);
    
    // Development tools
    if (isDev) {
        mainWindow.webContents.openDevTools();
    }

    // Handle window events
    ipcMain.on('dragging', (event, { x, y }) => {
        const position = mainWindow.getPosition();
        mainWindow.setPosition(position[0] + x, position[1] + y);
    });

    ipcMain.on('app-quit', () => {
        app.quit();
    });

    ipcMain.on('close-window', () => {
        const currentWindow = BrowserWindow.getFocusedWindow();
        if(currentWindow){
            currentWindow.close();
        }
    });

    ipcMain.on('minimize-window', () => {
        const currentWindow = BrowserWindow.getFocusedWindow();
        if(currentWindow){
            currentWindow.minimize();
        }
    });
}

app.whenReady().then(() => {
    startPythonBackend();
    createWindow();
});

app.on('window-all-closed', () => {
    if (pythonProcess) {
        pythonProcess.kill();
    }
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});