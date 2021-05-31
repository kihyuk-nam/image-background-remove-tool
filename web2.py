#web.py

from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

FILE_INPUT = "20210528-before.jpg"
FILE_OUTPUT = "20210528-after.png"
FILE_PATH = "/home/ubuntu/image-background-remove-tool/static/images/"
HOME_PATH = "/home/ubuntu/image-background-remove-tool/"

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
            arg = HOME_PATH + "nam-run2.sh " + fileInput + " " + fileOutput + " u2netp rtb-bnb" 
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
            # 1. POST /api/v0/files/key

            # 2. POST /api/v0/files/user_image

            # response
            return jsonify({'file_id': fileOutput, 'status': 200})

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
