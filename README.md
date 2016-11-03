# FileCarver
A PNG, PDF, JPG, DOC, and XLS file recovery tool project for our FORENSC class. <br/>
Written in Python that runs under the [Electron](http://electron.atom.io/) framework.<br/>

## Electron as GUI
The recovery of the files is written purely in **Python** that uses **Electron** as the "GUI shell" by embedding *flask* rendered web pages. <br/><br/>
More information about the program architecture can be found [here](https://www.fyears.org/2015/06/electron-as-gui-of-python-apps.html).

## Getting Started
This program requires [nodejs](https://nodejs.org/en/) and [Python](https://www.python.org/) installed in the machine.

### Prerequisites
Open the commands prompt as adminstrator to avoid permission denied issue. <br/>
Install flask to render web pages using Python.
```
pip install Flask
```
Install win32 module in Python to access drives.
```
pip install pypiwin32
```


## Installing
In the command line, go to the FileRecovery\app directory and install npm dependencies
```
npm install
```

## Run the Program
In the same directory, run the program by issuing "npm start"
```
npm start
```

## Note
**Normal and Deep scan option is still in progress.**

