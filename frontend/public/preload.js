const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electron', {
  ipcRenderer: {
    send: (channel, data) => {
      // Whitelist of channels that can be sent from renderer
      const validChannels = [
        'submit-text',
        'dragging',
        'minimize-window',
        'close-window',
        'open-main-window',
        'close-main-window',
        'openInputWindow',
        'update-game-id',
        'game-id-updated-success'
      ];
      if (validChannels.includes(channel)) {
        ipcRenderer.send(channel, data);
      }
    },
    on: (channel, func) => {
      // Whitelist of channels that can be received by renderer
      const validChannels = [
        'main-window-opened',
        'main-window-closed',
        'game-id-updated',
        'update-game-id'
      ];
      if (validChannels.includes(channel)) {
        // Remove any existing listeners to avoid duplicates
        ipcRenderer.removeAllListeners(channel);
        // Add the new listener
        ipcRenderer.on(channel, (event, ...args) => func(...args));
      }
    },
    removeListener: (channel, func) => {
      const validChannels = [
        'main-window-opened',
        'main-window-closed',
        'game-id-updated',
        'update-game-id'
      ];
      if (validChannels.includes(channel)) {
        ipcRenderer.removeListener(channel, func);
      }
    },
  }
});