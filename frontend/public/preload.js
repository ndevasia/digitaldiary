// preload.js

const { contextBridge, ipcRenderer } = require('electron');

// Expose a limited, secure API to the renderer process
contextBridge.exposeInMainWorld('electron', {
    ipcRenderer: {
        send: (channel, data) => ipcRenderer.send(channel, data),
        on: (channel, callback) => ipcRenderer.on(channel, callback)
    }
});