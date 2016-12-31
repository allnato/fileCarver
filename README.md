# FileCarver
A file recovery and drive shredder for our FORENSC class. <br/>
Written in Python that runs under the [Electron](http://electron.atom.io/) framework.<br/>

## Electron as GUI
The recovery and shredding programs are both written in **Python** that uses **Electron** as the "GUI shell" by embedding *flask* rendered web pages. <br/><br/>
More detailed information about the used system architecture -  [electron-as-gui-of-python-apps](https://www.fyears.org/2015/06/electron-as-gui-of-python-apps.html).

## Getting Started
This program requires [nodejs](https://nodejs.org/en/) and [Python 3.X](https://www.python.org/) installed in the machine.

### Prerequisites
Open the commands prompt as administrator to avoid permission denied issue. <br/>
Install flask to render web pages using Python.
```
pip install Flask
```
Install win32 module in Python to access drives.
```
pip install pypiwin32
```


## Installing
In the command line, go to the FileRecovery \app directory and install npm dependencies
```
npm install
```

## Run the Program
In the same directory, run the program by issuing "npm start"
```
npm start
```
