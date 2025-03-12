const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const isDev = require('electron-is-dev');
const { spawn } = require('child_process');

let mainWindow;  // Overlay window
let inputWindow; // Input window
let inputWindow;
let pythonProcess;
let gameName = '';

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

    inputWindow.loadFile(path.join(__dirname, 'input.html')); // Create a new HTML file for the input window
    // mainWindow.webContents.openDevTools(); // For debugging

    // When user submits the text, show the overlay window and close the input window
    ipcMain.on('submit-text', (event, game) => {
        // Store the game name in the main process
        gameName = game;
        console.log('Game name received:', gameName); // Test to see if the name passes through

        if (!mainWindow) {
            createOverlayWindow();  // Create the overlay window only when needed
        }

        if (mainWindow) {
            mainWindow.show();  // Show the overlay window
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

    mainWindow = new BrowserWindow({
        width: 800,
        height: 224,
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

    mainWindow.loadFile(path.join(__dirname, '../dist/index.html'));

    // Handle drag events
    ipcMain.on('dragging', (event, { x, y }) => {
        const position = mainWindow.getPosition();
        mainWindow.setPosition(position[0] + x, position[1] + y);
    });

    ipcMain.on('app-quit', () => {
        app.quit();
    });

    ipcMain.on('close-window', () => {
        const currentWindow = BrowserWindow.getFocusedWindow();
        if (currentWindow) {
            currentWindow.close();
        }
    });

    ipcMain.on('minimize-window', () => {
        const currentWindow = BrowserWindow.getFocusedWindow();
        if (currentWindow) {
            currentWindow.minimize();
        }
    });
}

app.whenReady().then(() => {
    createInputWindow();  // First create the input window
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
    }
});
