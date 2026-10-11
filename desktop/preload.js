const { contextBridge } = require('electron');

// Expose safe APIs to the renderer process
contextBridge.exposeInMainWorld('electron', {
  platform: process.platform,
  version: process.version
});

contextBridge.exposeInMainWorld('app', {
  name: 'Aurum Ventura Lead Finder',
  version: '1.0.0'
});
