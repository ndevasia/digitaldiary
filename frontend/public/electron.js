const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const isDev = require('electron-is-dev');
const { spawn } = require('child_process');
const fs = require('fs');

let overlayWindow;  // Overlay window
let inputWindow; // Input window
let mainWindow;
let pythonProcess;
let gameName = '';

function getPythonScriptPath() {
    if (isDev) {
        console.log("dev mode")
        return path.join(__dirname, "../../backend/window/app.py"); // Dev mode
    } else {
        console.log("prod mode")
        return path.join(backendPath, "/window/app.py"); // Production mode
    }
}

function startPythonBackend() {
    const scriptPath = getPythonScriptPath();
    console.log("Starting Python backend at:", scriptPath);

    pythonProcess = spawn("python", [scriptPath], {
        stdio: "inherit"
    });

    pythonProcess.on("error", (err) => {
        console.error("❌ Failed to start Python process:", err);
    });
}

function createInputWindow() {
    inputWindow = new BrowserWindow({
        width: 400,
        height: 200,
        frame: false,
        alwaysOnTop: true,
        transparent: true,
        backgroundColor: '#00ffffff',
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            preload: path.join(__dirname, 'preload.js')  // Set preload script
        }
    });

    inputWindow.loadFile(path.join(__dirname, 'input.html'));

    // When user submits the text, show the overlay window and close the input window
    ipcMain.on('submit-text', (event, game) => {
        // Store the game name in the main process
        gameName = game;
        console.log('Game name received:', gameName); // Test to see if the name passes through

        if (!overlayWindow) {
            createOverlayWindow();  // Create the overlay window only when needed
        }

        if (overlayWindow) {
            overlayWindow.show();  // Show the overlay window
        }

        if (inputWindow) {
            inputWindow.close();  // Close the input window
        }
    });
}

function createOverlayWindow() {
    const screen = require('electron').screen;
    const display = screen.getPrimaryDisplay();
    const { width } = display.workAreaSize;

    overlayWindow = new BrowserWindow({
        width: 64,
        height: 300,
        x: width - 100,
        y: 100,
        transparent: true,
        frame: false,
        alwaysOnTop: true,
        resizable: false,
        backgroundColor: '#00ffffff',
        hasShadow: false,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            nodeIntegration: false,
            contextIsolation: true,
        }
    });

    // Load the overlay UI
    const startUrl = isDev
        ? 'http://localhost:5173/?overlay=true'
        : `file://${path.join(__dirname, '../index.html?overlay=true')}`;

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

    ipcMain.on('minimize-window', () => {
        const currentWindow = BrowserWindow.getFocusedWindow();
        if (currentWindow) {
            currentWindow.minimize();
        }
    });
}

function createMainWindow() {
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            enableRemoteModule: true,
            preload: path.join(__dirname, 'preload.js')
        }
    });

    // Load the main React UI
    const startUrl = isDev
        ? 'http://localhost:5173/'
        : `file://${path.join(__dirname, '../index.html')}`;

    mainWindow.loadURL(startUrl);
    console.log("we are using startURL ", startUrl)

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

    ipcMain.on('openInputWindow', () => {
        createInputWindow();
    })
}

app.whenReady().then(() => {
    startPythonBackend();
    createMainWindow();
    //createOverlayWindow();
    //createInputWindow();
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
        createInputWindow();
        createOverlayWindow();
        createMainWindow()
    }
});
