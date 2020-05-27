# coding:utf-8
import datetime
from datetime import timedelta
from werkzeug.utils import secure_filename
from flask import Flask, render_template, jsonify, request, make_response, send_from_directory, abort, Response
import time
import os
import base64
import random
import csv
import codecs


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def create_uuid(): #生成唯一的图片的名称字符串，防止图片显示时的重名问题
    nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
    randomNum = random.randint(0, 100);  # 生成的随机整数n，其中0<=n<=100
    if randomNum <= 10:
        randomNum = str(0) + str(randomNum);
    uniqueNum = str(nowTime) + str(randomNum);
    return uniqueNum;


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

basedir = os.path.abspath(os.path.dirname(__file__))
 

@app.route('/up_photo', methods=['POST'], strict_slashes=False)
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['photo']
    if f and allowed_file(f.filename):
        fname = secure_filename(f.filename)
        print (fname)
        ext = fname.rsplit('.', 1)[1]
        new_filename = create_uuid() + '.' + ext
        f.save(os.path.join(file_dir, new_filename)) 
        return jsonify({"success": 0, "msg": "http://localhost:5000/show/"+new_filename})
    else:
        return jsonify({"error": 1001, "msg": "上传失败"})

@app.route('/leave-message', methods=['POST'], strict_slashes=False)
def leave_message():
    message = request.get_json()
    f = codecs.open('message.csv','a+','gbk')
    writer = csv.writer(f)
    localtime = time.asctime(time.localtime(time.time()))
    writer.writerow([message["comment"],str(localtime),str(request.remote_addr)])
    f.close()
    return jsonify({"success": 0, "msg": "更新成功"})

@app.route('/get-message', methods=['GET'], strict_slashes=False)
def get_message():
    returnedData = {
        "messages":[]
    }
    with codecs.open('message.csv', 'rb', 'gbk') as f:
        for i in f:
            returnedData["messages"].append(i)
    print (returnedData)
    response = make_response(returnedData, 200)
    return response


if __name__ == '__main__':
    app.run(debug=True)
