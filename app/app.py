import sys, os
sys.path.append('../')
from head_file import *
from init_drive import *
from model_app import *
from flask import Flask, render_template, request, redirect
app = Flask(__name__)

# Global Variables
seletedDrive = None
copyRawPath = None
copyRawName = None

# Start page of the application
@app.route("/")
def start():
    return render_template('start.html')

# Select a drive page.
@app.route("/select", methods=['GET','POST'])
def select():
    return render_template('select.html', drive_list = listDrive())

# Set the user input in the select page
@app.route("/setSelect", methods=['GET', 'POST'])
def setSelectGlobal():
    drive = request.form['drive']
    path = request.form['copyPath']
    name = request.form['copyName']
    setSelect(drive, path, name)
    print(selectedDrive, file=sys.stderr)
    print(copyRawPath, file=sys.stderr)
    print(copyRawName, file=sys.stderr)
    if not name or not path :
        print('redirect to config', file=sys.stderr)
        return redirect('http://localhost:5000/config')
    else:
        print('redirect to copy', file=sys.stderr)
        return redirect('http://localhost:5000/copy')

# Configure extraction page.
@app.route("/config", methods=['GET','POST'])
def config():
    return render_template('config.html')

# Copy raw image loading page.
@app.route("/copy", methods=['GET','POST'])
def copy():
    return render_template('loadCopy.html')

# Extract retireved files loading page.
@app.route("/extract", methods=['GET','POST'])
def extract():
    return render_template('loadExtract.html')

def setSelect(drive, rawPath = None, rawName = None):
    global selectedDrive
    global copyRawPath
    global copyRawName
    selectedDrive = drive
    copyRawName = rawName
    copyRawPath = rawPath

if __name__ == "__main__":
    print('Starting...')
    sys.stdout.flush()
    app.run()
