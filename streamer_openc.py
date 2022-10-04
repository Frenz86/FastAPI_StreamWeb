import cv2
import base64
import json
import requests
import imutils

class BytesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode('utf-8')
        return json.JSONEncoder.default(self, obj)

url = "http://localhost:8000/send_frame_from_string/stream002" 

cam = cv2.VideoCapture(0)

while (True):
    ret, frame = cam.read()
    frame = imutils.resize(frame, width=320)                     # get frame from webcam
    res, frame = cv2.imencode('.jpg', frame)    # from image to binary buffer
    base64str = base64.b64encode(frame)              # convert to base64 format
    payload = json.dumps({"img_base64str": base64str}, cls=BytesEncoder)
    response = requests.post(url,data = payload,stream=True)                     # send to server
