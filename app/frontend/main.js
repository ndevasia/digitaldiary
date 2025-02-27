const { app, BrowserWindow } = require("electron");
const { spawn } = require("child_process");
const path = require("path");
const http = require("http");

let mainWindow;
let flaskProcess;
const FLASK_URL = "http://127.0.0.1:5000"; // Flask server URL

// function getFlaskExecutablePath() {
//     if (process.env.NODE_ENV === "development") {
//         return path.join(__dirname, "../backend/dist/server.exe"); // Dev mode
//     } else {
//         return path.join(process.resourcesPath, "backend/dist/server.exe"); // Production mode
//     }
// }

function startFlaskBackend() {
    const flaskPath = "C:/Users/ndevasia/projects/digitaldiary/app/backend/dist/server.exe"
    console.log("Starting Flask backend at:", flaskPath);

    try {
        flaskProcess = spawn(flaskPath, { stdio: "inherit" });

        flaskProcess.on("error", (err) => {
            console.error("❌ Failed to start Flask backend:", err);
        });

        flaskProcess.on("close", (code) => {
            console.error(`⚠️ Flask process exited with code ${code}`);
        });
    } catch (error) {
        console.error("❌ Flask startup error:", error);
    }
}

// Function to check if Flask is ready
function checkFlaskReady(callback) {
    http.get(FLASK_URL, (res) => {
        if (res.statusCode === 200) {
            console.log("✅ Flask is ready!");
            callback(true);
        } else {
            console.log("⏳ Waiting for Flask...");
            setTimeout(() => checkFlaskReady(callback), 1000);
        }
    }).on("error", () => {
        console.log("⏳ Waiting for Flask...");
        setTimeout(() => checkFlaskReady(callback), 1000);
    });
}

function createWindow() {
    console.log("🚀 Creating Electron window...");

    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    console.log("🌐 Loading Flask frontend from", FLASK_URL);
    mainWindow.loadURL(FLASK_URL);

    mainWindow.webContents.on("did-fail-load", (event, errorCode, errorDescription) => {
        console.error("❌ Failed to load Flask frontend:", errorDescription);
    });

    mainWindow.webContents.on("did-finish-load", () => {
        console.log("✅ Flask frontend successfully loaded!");
    });

    mainWindow.on("closed", () => {
        console.log("🛑 Electron window closed.");
        if (flaskProcess) flaskProcess.kill();
    });
}

app.whenReady().then(() => {
    startFlaskBackend(); // Start Flask backend
    checkFlaskReady(() => {
        createWindow(); // Only open Electron when Flask is fully started
    });
});

app.on("window-all-closed", () => {
    if (process.platform !== "darwin") {
        if (flaskProcess) {
            console.log("🛑 Killing Flask process...");
            flaskProcess.kill();
        }
        console.log("👋 Quitting Electron app...");
        app.quit();
    }
});
