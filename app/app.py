import sys, os, time
sys.path.append('../controller')
from head_file import *
from init_drive import *
from model_app import *
from flask import Flask, render_template, request, redirect, jsonify, Response
app = Flask(__name__)

# Global Variables
selectedDrive = None
copyRawPath = None
copyRawName = None

fileList = None
filePrefix = ""
scanOption = None
extractLocation = None

fullDriveList = None

# Start page of the application
@app.route("/")
def start():
    return render_template('start.html')

# Select a drive page.
@app.route("/select", methods=['GET','POST'])
def select():
    global fullDriveList
    fullDriveList = listDrive()
    return render_template('select.html', drive_list = fullDriveList)

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
    sys.stdout.flush()
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
    setConfig(request.form.getlist('checklist'),request.form['scanOption'],
    request.form['extractLocation'], request.form['filePrefix'])

    # Call compileRegs
    (lst_srt, lst_end, lst_buf) = compileRegs(fileList)
    # CompileRegs Debug
    print(lst_srt, file=sys.stderr)
    print(lst_end, file=sys.stderr)
    print(lst_buf, file=sys.stderr)

    # get Drive Location
    drive = getDrive(fullDriveList, int(selectedDrive))

    print(drive, file=sys.stderr)
    print(extractLocation, file=sys.stderr)
    print(fileList, file=sys.stderr)
    print(scanOption, file=sys.stderr)

    if scanOption == "1":
        print('hi', file=sys.stderr)
        fullPrefix = namingFile(extractLocation, filePrefix)
        fastReadImage(drive, fullPrefix, lst_srt, lst_end, fileList, lst_buf)
    print('hello', file=sys.stderr)

    return render_template('loadExtract.html')

@app.route('/jURL')
def ajax():
    result = "Hello"
    return jsonify(result)

@app.route('/progress')
def progress():
    def generate():
        x = 0
        while x < 100:
            print (x)
            x = x + 1
            time.sleep(0.1)
            yield "data:" + str(x) + "\n\n"
    return Response(generate(), mimetype= 'text/event-stream')

# Set the drive, rawpath, and rawname global variables.
def setSelect(drive, rawPath = None, rawName = None):
    global selectedDrive
    global copyRawPath
    global copyRawName
    selectedDrive = drive
    copyRawName = rawName
    copyRawPath = rawPath

def setConfig(listFile, option, location, prefix = ""):
    global fileList
    global filePrefix
    global scanOption
    global extractLocation
    fileList = listFile
    filePrefix = prefix
    scanOption = option
    extractLocation = location

if __name__ == "__main__":
    print('Starting...')
    sys.stdout.flush()
    app.run()
