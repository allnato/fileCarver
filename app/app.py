import sys
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def start():
    return render_template('start.html')

@app.route("/select", methods=['GET','POST'])
def select():
    return render_template('select.html')

@app.route("/config", methods=['GET','POST'])
def config():
    print('The configuration Page', file=sys.stderr)
    return render_template('config.html')

@app.route("/copy", methods=['GET','POST'])
def copy():
    return render_template('loadCopy.html')

if __name__ == "__main__":
    print('Starting...')
    sys.stdout.flush()
    app.run()
