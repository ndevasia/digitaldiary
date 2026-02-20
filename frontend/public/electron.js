const { app, BrowserWindow, ipcMain, screen } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs');

let overlayWindow;
let mainWindow;
let pythonProcess;

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
        // Use the virtual environment Python if it exists
        const venvPython = path.join(__dirname, "../../venv/Scripts/python.exe");
        const pythonCmd = fs.existsSync(venvPython) ? venvPython : "python";
        
        console.log("Using Python:", pythonCmd);
        pythonProcess = spawn(pythonCmd, [scriptPath], {
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

function createOverlayWindow() {
    const display = screen.getPrimaryDisplay();
    const { width } = display.workAreaSize;

        overlayWindow = new BrowserWindow({
            width: 64,
            height: 300,
            minWidth: 64,
            minHeight: 100,
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

    // Ensure overlayWindow reference is cleared when it's closed
    overlayWindow.on('closed', () => {
        overlayWindow = null;
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
        if (overlayWindow && overlayWindow.webContents && !overlayWindow.webContents.isDestroyed()) {
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

        // Resizing: main process uses global cursor position
        let resizeInterval = null;

        ipcMain.on('start-resize', () => {
            if (!overlayWindow) return;
            const startMouse = screen.getCursorScreenPoint();
            const startBounds = overlayWindow.getBounds();

            if (resizeInterval) clearInterval(resizeInterval);
            resizeInterval = setInterval(() => {
                const currentMouse = screen.getCursorScreenPoint();
                const newWidth = Math.max(64, startBounds.width + (currentMouse.x - startMouse.x));
                const newHeight = Math.max(100, startBounds.height + (currentMouse.y - startMouse.y));
                overlayWindow.setResizable(true);
                overlayWindow.setSize(Math.round(newWidth), Math.round(newHeight));
                overlayWindow.setResizable(false);
            }, 16);

            ipcMain.once('stop-resize', () => {
                clearInterval(resizeInterval);
                resizeInterval = null;
            });
        });

    ipcMain.on('open-main-window', () => {
        if (!mainWindow) {
            createMainWindow();
        } else {
            mainWindow.show();
            mainWindow.focus();
        }

        // Notify the overlay window that the main window is open
        if (overlayWindow && overlayWindow.webContents && !overlayWindow.webContents.isDestroyed()) {
            overlayWindow.webContents.send('main-window-opened');
        }
    });

    ipcMain.on('close-main-window', () => {
        if (mainWindow) {
            mainWindow.close();
            // Notify the overlay window that the main window is closed
            if (overlayWindow && overlayWindow.webContents && !overlayWindow.webContents.isDestroyed()) {
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