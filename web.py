#web.py

from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

FILE_INPUT = "20210517-before.jpg"
FILE_OUTPUT = "20210517-after.png"
FILE_PATH = "/home/ubuntu/image-background-remove-tool/static/images/"
HOME_PATH = "/home/ubuntu/image-background-remove-tool/"

@app.route("/hello")
def hello():
    return "Hello"

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/background-remove', methods=['POST'])
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
            arg = HOME_PATH + "nam-run2.sh " + fileInput + " " + fileOutput + " u2netp rtb-bnb" 
            p = subprocess.Popen(arg, stdout=subprocess.PIPE, shell=True)
            return jsonify({'file_id': fileOutput, 'status': 200}) # TODO upload the result to S3 and return the id

if __name__ == '__main__': 
    app.run(debug=True)
# 또는 80 포트 사용하고 싶다면, root 상태에서 아래 실행
#    app.run(host='0.0.0.0', port=80)
