from flask import Flask, render_template
from datetime import timedelta

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/cross')
def cross():
    return render_template('cross.html')

@app.route('/gdesign')
def gdesign():
    return render_template('gdesign.html')

@app.route('/transfer')
def transfer():
    return render_template('transfer.html')

if __name__ == '__main__':
    app.run(debug=True)
