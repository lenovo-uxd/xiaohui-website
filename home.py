# coding:utf-8
import datetime
from datetime import timedelta
from werkzeug.utils import secure_filename
from flask import Flask, render_template, jsonify, request, make_response, send_from_directory, abort, Response, send_from_directory

import time
import os
import base64
import random
import codecs
import requests
import csv
import json
import pandas as pd
from flask_cors import CORS

token = "c5f583ba-d03c-4e84-bc7a-7a4250037c87"


app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF', 'pdf', 'PDF'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def create_uuid(): #生成唯一的图片的名称字符串，防止图片显示时的重名问题
    nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
    randomNum = random.randint(0, 100);  # 生成的随机整数n，其中0<=n<=100
    if randomNum <= 10:
        randomNum = str(0) + str(randomNum);
    uniqueNum = str(nowTime) + str(randomNum);
    return uniqueNum;



@app.route('/other-upload/<path:path>')
def send_js(path):
    return send_from_directory('other-upload', path)

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

@app.route('/api')
def api():
    return render_template('api.html')

basedir = os.path.abspath(os.path.dirname(__file__))
 
headers = {
  'Content-Type': 'application/json'
}


@app.route('/upload', methods=['POST'], strict_slashes=False)
def api_upload_file():
    UPLOAD_FOLDER = 'other-upload'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['file']
    if f and allowed_file(f.filename):
        fname = secure_filename(f.filename)
        print (fname)
        ext = fname.rsplit('.', 1)[1]
        
        f.save(os.path.join(file_dir, fname)) 
        return jsonify({"success": 0, "msg": "http://xiaohui.ai/other-upload/"+fname})
    else:
        return jsonify({"error": 1001, "msg": "上传失败"})

@app.route('/up_photo', methods=['POST'], strict_slashes=False)
def api_upload():
    UPLOAD_FOLDER = 'upload'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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
    with open('message.csv', 'a+') as csvfile:
        fieldnames = ['content', 'time','ip']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        localtime = time.asctime(time.localtime(time.time()))
        writer.writerow({'content': message["comment"], 'time': str(localtime), 'ip':str(request.remote_addr)})
        csvfile.close()
        return jsonify({"success": 0, "msg": "更新成功"})


@app.route('/get-message', methods=['GET'], strict_slashes=False)
def get_message():
    returnedData = {
        'comment':[]
    }
    data = pd.read_csv('message.csv',encoding='utf-8')
    for i in range(len(data)):
        returnedData['comment'].append(data["content"][i])
    return jsonify(returnedData)

#图片风格转换
@app.route('/style-transfer', methods=['POST'])
def style_transfer():
    data = json.dumps(request.get_json())
    #url = "http://10.110.146.100:11354/apicore/art/style-transfer-simple-graph/1.0.0"
    url = "https://api.brain.lenovo.com/lenovo/ad/style-transfer-service/1.0?token="+token
    res = requests.post(url=url,headers=headers,data=data)
    return jsonify(json.loads(res.content))

#头像域到域转换
@app.route('/cross-domain', methods=['POST'])
def cross_domain():
    data = json.dumps(request.get_json())
    #url = "http://10.110.146.100:11354/apicore/art/cross-domain-align/1.0.0"
    url = "https://api.brain.lenovo.com/lenovo/ad/art-portrait-service/1.0?token="+token
    res = requests.post(url=url,headers=headers,data=data)
    return jsonify(json.loads(res.content))

#随机生成图像
@app.route('/style-gan-random', methods=['POST'])
def style_gan_random():
    data = json.dumps(request.get_json())
    #url = "http://10.110.146.100:11354/apicore/art/style-gan-random/1.0.0"
    url = "https://api.brain.lenovo.com/lenovo/ad/abstract-art-service/1.0?token="+token
    res = requests.post(url=url,headers=headers,data=data)
    return jsonify(json.loads(res.content))

#拓展图像
@app.route('/style-gan-extend', methods=['POST'])
def style_gan_extend():
    data = json.dumps(request.get_json())
    #url = "http://10.110.146.100:11354/apicore/art/style-gan-withtag/1.0.0"
    url = "https://api.brain.lenovo.com/lenovo/ad/semantic-art-design/1.0?token="+token
    res = requests.post(url=url,headers=headers,data=data)
    return jsonify(json.loads(res.content))


#随机生成图像
@app.route('/style-gan-random-localtest', methods=['POST'])
def style_gan_random_test():
    data = json.dumps(request.get_json())
    url = "http://10.110.146.100:11354/apicore/art/style-gan-random/1.0.0"
    # url = "https://api.brain.lenovo.com/lenovo/ad/abstract-art-service/1.0?token="+token
    res = requests.post(url=url,headers=headers,data=data)
    return jsonify(json.loads(res.content))

#拓展图像
@app.route('/style-gan-extend-localtest', methods=['POST'])
def style_gan_extend_test():
    data = json.dumps(request.get_json())
    url = "http://10.110.146.100:11354/apicore/art/style-gan-withtag/1.0.0"
    # url = "https://api.brain.lenovo.com/lenovo/ad/semantic-art-design/1.0?token="+token
    res = requests.post(url=url,headers=headers,data=data)
    return jsonify(json.loads(res.content))





if __name__ == '__main__':
    app.run(debug=True,port=3002,host='0.0.0.0')
