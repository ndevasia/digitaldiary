const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');

const { spawn } = require('child_process');
const fs = require('fs');

let overlayWindow;  // Overlay window
let inputWindow; // Input window
let mainWindow;
let pythonProcess;
let gameName = '';

// Check if we're in development mode
const isDev = process.env.NODE_ENV === 'development' || !app.isPackaged;

function getPythonScriptPath() {
    if (isDev) {
        console.log("dev mode")
        return path.join(__dirname, "../../backend/window/app.py"); // Dev mode
    } else {
        console.log("prod mode")
        const serverPath = path.join(process.resourcesPath, 'server.exe');
        console.log("Server path:", serverPath);

        // Verify the server.exe exists
        if (!fs.existsSync(serverPath)) {
            console.error("❌ server.exe not found at:", serverPath);
            console.log("Available files in resources:", fs.readdirSync(process.resourcesPath));
        } else {
            console.log("✅ server.exe found at:", serverPath);
        }

        return serverPath;
    }
}

function startPythonBackend() {
    const scriptPath = getPythonScriptPath();
    console.log("Starting Python backend at:", scriptPath);

    if (isDev) {
        pythonProcess = spawn("python", [scriptPath], {
            stdio: "inherit"
        });

        pythonProcess.on("error", (err) => {
            console.error("❌ Failed to start Python process:", err);
        });
    } else {
        try {
            console.log("Attempting to start server.exe...");
            pythonProcess = spawn(scriptPath, [], {
                stdio: ['pipe', 'pipe', 'pipe'],
                shell: true,
                cwd: path.dirname(scriptPath)
            });

            pythonProcess.stdout.on('data', (data) => {
                console.log(`Server stdout: ${data}`);
            });

            pythonProcess.stderr.on('data', (data) => {
                console.error(`Server stderr: ${data}`);
            });

            pythonProcess.on("error", (err) => {
                console.error("❌ Failed to start server:", err);
            });

            pythonProcess.on("close", (code) => {
                console.error(`⚠️ Server process exited with code ${code}`);
            });
        } catch (error) {
            console.error("❌ Server startup error:", error);
        }
    }
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

    if (isDev) {
        const startUrl = 'http://localhost:5173/?overlay=true';
        console.log("Loading overlay URL:", startUrl);
        overlayWindow.loadURL(startUrl);
    } else {
        const filePath = path.join(__dirname, '..', 'dist', 'index.html');
        console.log("Loading overlay file:", filePath);
        overlayWindow.loadFile(filePath, { query: { overlay: 'true' } });
    }


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

    if (isDev) {
        const startUrl = 'http://localhost:5173/';
        console.log("Loading main URL:", startUrl);
        mainWindow.loadURL(startUrl);
    } else {
        const filePath = path.join(__dirname, '..', 'dist', 'index.html');
        console.log("Loading main file:", filePath);
        console.log("File exists:", fs.existsSync(filePath));
        console.log("Directory contents:", fs.readdirSync(path.dirname(filePath)));

        // Try with a query parameter to see if that helps
        mainWindow.loadFile(filePath, { query: { main: 'true' } });

        // Add event listeners to see what's happening
        mainWindow.webContents.on('did-fail-load', (event, errorCode, errorDescription) => {
            console.error('Failed to load:', errorCode, errorDescription);
        });

        mainWindow.webContents.on('did-finish-load', () => {
            console.log('Main window loaded successfully');
        });
    }

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
