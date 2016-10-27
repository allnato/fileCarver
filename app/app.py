import sys
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def start():
    return render_template('start.html')

@app.route("/config", methods=['GET','POST'])
def config():
    return render_template('config.html')

if __name__ == "__main__":
    print('Starting...')
    sys.stdout.flush()
    app.run()
