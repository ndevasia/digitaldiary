const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const isDev = require('electron-is-dev');
const { spawn } = require('child_process');

let overlayWindow;
let mainWindow;
let pythonProcess;

function startPythonBackend() {
    pythonProcess = spawn('python', ['../lib/window/app.py'], {
        stdio: 'inherit'
    });

    pythonProcess.on('error', (err) => {
        console.error('Failed to start Python process:', err);
    });
}

function createOverlayWindow() {
    const screen = require('electron').screen;
    const display = screen.getPrimaryDisplay();
    const { width } = display.workAreaSize;

    overlayWindow = new BrowserWindow({
        width: 64,     // w-16 == 64 Width for icons (16px * 4)
        height: 300,    // h-56 == 224 Height for 3 icons + close button + spacing
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

    // Load the overlay UI
    const startUrl = isDev 
        ? 'http://localhost:5173/?overlay=true' 
        : `file://${path.join(__dirname, '../dist/index.html?overlay=true')}`;
        
    overlayWindow.loadURL(startUrl);
    
    if (isDev) {
        overlayWindow.webContents.openDevTools({ mode: 'detach' });
    }

    // Handle drag events for overlay
    ipcMain.on('dragging', (event, { x, y }) => {
        if (overlayWindow) {
            const position = overlayWindow.getPosition();
            overlayWindow.setPosition(position[0] + x, position[1] + y);
        }
    });
}

function createMainWindow() {
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
            enableRemoteModule: true
        }
    });

    // Load the main React UI
    const startUrl = isDev 
        ? 'http://localhost:5173/' 
        : `file://${path.join(__dirname, '../dist/index.html')}`;
        
    mainWindow.loadURL(startUrl);
    
    if (isDev) {
        mainWindow.webContents.openDevTools();
    }

    mainWindow.on('closed', () => {
        mainWindow = null;
        // Notify the overlay window that the main window is closed
        if (overlayWindow) {
            overlayWindow.webContents.send('main-window-closed');
        }
    });
}

// Handle IPC messages
function setupIPC() {
    ipcMain.on('app-quit', () => {
        app.quit();
    });

    ipcMain.on('close-window', () => {
        const currentWindow = BrowserWindow.getFocusedWindow();
        if(currentWindow) {
            currentWindow.close();
        }
    });

    ipcMain.on('minimize-window', () => {
        const currentWindow = BrowserWindow.getFocusedWindow();
        if(currentWindow) {
            currentWindow.minimize();
        }
    });

    ipcMain.on('open-main-window', () => {
        if (!mainWindow) {
            createMainWindow();
        } else {
            mainWindow.show();
            mainWindow.focus();
        }
        
        // Notify the overlay window that the main window is open
        if (overlayWindow) {
            overlayWindow.webContents.send('main-window-opened');
        }
    });

    ipcMain.on('close-main-window', () => {
        if (mainWindow) {
            mainWindow.close();
            // Notify the overlay window that the main window is closed
            if (overlayWindow) {
                overlayWindow.webContents.send('main-window-closed');
            }
        }
    });
}


app.whenReady().then(() => {
    startPythonBackend();
    createOverlayWindow();
    createMainWindow();
    setupIPC();
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
        createOverlayWindow();
        createMainWindow();
    }
});