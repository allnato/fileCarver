const electron = require('electron');
// Module to control application life.
const app = electron.app;
// Module to create native broweser window.
const BrowserWindow = electron.BrowserWindow;

// Global reference of the window Object.
var mainWindow = null;

// This method will be invoked if electron is done loading.
app.on('ready', function(){
  // Call Python/Flask
  var subpy = require("child_process").spawn('python', ['./app.py'], {detached: true});

  var rq = require('request-promise');
  var mainAddr = 'http://localhost:5000';

  var openWindow = function(){
    // Create the browser window.
    mainWindow = new BrowserWindow({width: 1024, height: 768, show: false});

    // Loads localhost:5000 (Flask)
    mainWindow.loadURL('http://localhost:5000');
    
    // Only show native window if elements are ready.
    mainWindow.on('ready-to-show', function(){
      mainWindow.show();
    })

    // Invoked when the window is closed.
    mainWindow.on('closed', function() {
      mainWindow = null;
      // kill Python program.
      subpy.kill('SIGINT');
    });

    subpy.stdout.on('data', function(data){
      console.log(data.toString());
    });
  };

  var startUp = function(){
    rq(mainAddr)
      .then(function(htmlString){
        console.log('Server started!');
        openWindow();
      })
      .catch(function(err){
        console.log('Error in starting the server.');
        openWindow();
      });
  };

  // fire!
  startUp();
});

// Quit when all windows are clsoed.
app.on('window-all-closed', function() {
  // For MAC
  if (process.platform != 'darwin') {
    app.quit();
  }
});
