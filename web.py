#web.py

# for providing web interface
from flask import Flask, render_template, request, jsonify
import subprocess
# for calling backend api
import requests
from requests.auth import HTTPBasicAuth
import json
from pathlib import Path

app = Flask(__name__)

HOME_PATH = "/home/ubuntu/image-background-remove-tool/"
FILE_DIR = "static/images/"
FILE_INPUT = "IN-20210531.jpg"
FILE_OUTPUT = "OUT-20210531.png"
#FILE_PATH = "/home/ubuntu/image-background-remove-tool/static/images/"
FILE_PATH = HOME_PATH + FILE_DIR
FILE_OUTPUT_PATH = FILE_PATH + FILE_OUTPUT

URL_HOME = "http://api-develop.miricanvas.com"
URL_KEY = "/api/v0/files/key"
URL_USER_IMAGE = "/api/v0/files/user_image/" # CAUTION!! if the '/' at the end is removed, error occures

# Set Cookies: miri_access=xxxx
COOKIE = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhY2NvdW50X2lkIjo2MzYsImNzX21vZGUiOmZhbHNlLCJleHAiOjE2MjI0NTI2MDd9.I-XlB8-uFPO5g5o6t6vDZZIczJWQzstCzgsZBzgWb8A'

@app.route("/hello")
def hello():
    return "Hello"

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/background-remove', methods=['POST']) # TODO /transform
def background_remove():
    if request.method == 'POST':
        file = request.files['file']
        if file is not None:
            print(file.filename)
            fileInput = FILE_PATH + FILE_INPUT
            fileOutput = FILE_PATH + FILE_OUTPUT
            print("Input file will be saved as " + fileInput)
            print("Output file will be saved as " + fileOutput)
            file.save(fileInput)

            # execute the remover
            arg = HOME_PATH + "run-remover.sh " + fileInput + " " + fileOutput + " u2netp rtb-bnb" 
            print("Execute remove : " + arg)
            p = subprocess.Popen(arg, stdout=subprocess.PIPE, shell=True)
            #p.wait() # wait until the job finished

            # import asyncio
            # proc = await asyncio.create_subprocess_shell(
            #        arg, 
            #        stdout=asyncio.subprocess.PIPE,
            #        stderr=asyncio.subprocess.PIPE)
            # # try: await asyncio.wait_for(...)
            # # except asyncio.TimeoutError: print('timeout!')
            # stdout, stderr = await proc.communicate()
            # print(f'[{cmd!r} exited with {proc.returncode}]')
            # if stdout:
            #   print(f'[stdout]\n{stdout.decode()}')
            # if stderr:
            #   print(f'[stderr]\n{stderr.decode()}')

            # TODO 
            # upload the result to S3 and return the id
            # 0. set cookie value
            cookies = dict(miri_access=COOKIE)

            # 1. POST /api/v0/files/key
            #  - Get UUID for a image
            resp = requests.post(URL_HOME+URL_KEY, cookies=cookies)
            print(resp.text)
            uuid = str(resp.json()["data"])
            print(uuid)

            # 2. POST /api/v0/files/user_image
            # Upload file
            p.wait() # wait until the job finished
            f = open(FILE_OUTPUT_PATH, 'rb')
            data  = {'key': uuid, 
                     'teamIdx': '518', 'teamScope': 'INDIVIDUAL', 'extraData': '{"width":960,"height":1280}'}
            files = {"file": f}
            resp = requests.post(URL_HOME+URL_USER_IMAGE, files=files, data=data, cookies=cookies)
            print(resp.text)
            print("status code " + str(resp.status_code))

            if resp.status_code == 200:
              print("Success")
              data = json.loads(resp.text)
              results = data['data']
              file_key = results['fileKey']
              file_url = results['originUrl']
              print (file_key)
              print (file_url)
            else:
              print ("Failure")

            # response
            return jsonify({'file_id': uuid, 'status': 200})

#// 브라우저 캐시 끄기 : 매번 새 이미지 불러오도록
@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

if __name__ == '__main__': 
    app.run(debug=True)
# 또는 80 포트 사용하고 싶다면, root 상태에서 아래 실행
#    app.run(host='0.0.0.0', port=80)
