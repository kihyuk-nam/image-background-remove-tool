import requests
from requests.auth import HTTPBasicAuth
import json
from pathlib import Path

HOME_PATH = "/home/ubuntu/image-background-remove-tool"
FILE_DIR  = "/static/images"
FILE_INPUT = "/20210528-before.jpg"
FILE_OUTPUT = "/20210528-after.png"
FILE_OUTPUT_PATH = HOME_PATH + FILE_DIR + FILE_OUTPUT

URL_HOME = "http://api-develop.miricanvas.com"
URL_KEY = "/api/v0/files/key"
URL_USER_IMAGE = "/api/v0/files/user_image/"

# Set Cookies: miri_access=xxxx
value = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhY2NvdW50X2lkIjo2MzYsImNzX21vZGUiOmZhbHNlLCJleHAiOjE2MjIxOTY4MDB9.HuMlKz7ZGj92eUC1yWp3I3Zlf8gvMlBY60Xgs3VGK_w'
cookies = dict(miri_access=value)

# Get UUID for a image
resp = requests.post(URL_HOME+URL_KEY, cookies=cookies)
print(resp.text)
uuid = str(resp.json()["data"])
print(uuid)

# Upload file
f = open(FILE_OUTPUT_PATH, 'rb')
data  = {'key': uuid, 'teamIdx': '518', 'teamScope': 'INDIVIDUAL', 'extraData': '{"width":960,"height":1280}'} 
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
