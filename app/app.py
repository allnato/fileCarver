import sys, os, time
sys.path.append('../controller')
from head_file import *
from init_drive import *
from model_app import *
from flask import Flask, render_template, request, redirect, jsonify, Response
app = Flask(__name__)

# Global Variables
doCopy = None
selectedDrive = None
copyRawPath = None
copyRawName = None

fileList = None
filePrefix = ""
scanOption = None
extractLocation = None

fullDriveList = None

drive = None

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

#  Select a raw image Page
@app.route("/selectRaw", methods=['GET','POST'])
def selectRaw():
    return render_template('selectRaw.html')

# Set the user input in the select page
@app.route("/setSelect", methods=['GET', 'POST'])
def setSelectGlobal():
    global drive
    driveText = request.form['drive']
    path = request.form['copyPath']
    name = request.form['copyName']
    copy = request.form['copy']
    setSelect(driveText, copy, path, name)
    # print(selectedDrive, file=sys.stderr)
    # print(copyRawPath, file=sys.stderr)
    # print(copyRawName, file=sys.stderr)
    # print(option, file=sys.stderr)
    # sys.stdout.flush()

    drive = getDrive(fullDriveList, int(selectedDrive))
    print(drive, file=sys.stderr)
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

    #print(drive, file=sys.stderr)
    print(extractLocation, file=sys.stderr)
    print(fileList, file=sys.stderr)
    print(scanOption, file=sys.stderr)

    if scanOption == "1":
        print('[+] Initializing Fast Scan', file=sys.stderr)
    elif scanOption == "2":
        print('[+] Initializing Normal Scan', file=sys.stderr)
    elif scanOption == "3":
        print('[+] Initializing Deep Scan', file=sys.stderr)

    rawExtractLocation = extractLocation.replace('\\','\\\\')
    print(rawExtractLocation, file=sys.stderr)
    return render_template('loadExtract.html', copy = doCopy, location = rawExtractLocation)

# Extract directly from drive
@app.route('/scanExtract')
def scanExtract():
    (lst_srt, lst_end, lst_buf) = compileRegs(fileList)
    if scanOption == '1':
        print ('Extracting (Fast-Scan): ', file=sys.stderr)
        fullPrefix = namingFile(extractLocation, filePrefix)
        return Response(fastReadImage(drive, fullPrefix, lst_srt, lst_end, fileList, lst_buf),
        mimetype= 'text/event-stream')

# Extract from copied raw Image
@app.route('/scanExtractCopy')
def scanCopy():
    rawPath = copyRawPath + copyRawName + ".dd"
    print (rawPath, file=sys.stderr)
    (lst_srt, lst_end, lst_buf) = compileRegs(fileList)
    if scanOption == '1':
        print ('Extracting (Fast-Scan): ', file=sys.stderr)
        fullPrefix = namingFile(extractLocation, filePrefix)
        return Response(fastReadImage(rawPath, fullPrefix, lst_srt, lst_end, fileList, lst_buf),
        mimetype= 'text/event-stream')


# Copy Raw Image
@app.route("/copyImage")
def copyImage():
    return Response(toRawImage(copyRawName, copyRawPath, drive), mimetype= 'text/event-stream')




# Set the drive, rawpath, and rawname global variables.
def setSelect(drive, copy, rawPath = None, rawName = None):
    global selectedDrive
    global copyRawPath
    global copyRawName
    global doCopy
    selectedDrive = drive
    doCopy = copy
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
