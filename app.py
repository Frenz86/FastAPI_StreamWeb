import streamlit as st
import cv2
import json
import base64
import requests

class BytesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode('utf-8')
        return json.JSONEncoder.default(self, obj)

st.title("Project")

# load OpenCV's Haar cascade for face detection from disk
#haar = "haarcascade_frontalface_default.xml"
#detector = cv2.CascadeClassifier(haar)

# initialize the video stream
"Starting video stream..."

selection = st.radio("Select option", options=['only camera','camera+ api'])

# Create text input for user entry
if selection == "only camera": 
    st.write("selexionato uno")

    @st.cache(allow_output_mutation=True)
    def get_cap():
        return cv2.VideoCapture(0)

    cap = get_cap()

    frameST = st.empty()

    # loop over the frames from the video stream
    while True:
        ret, frame = cap.read()

        # # detect faces in the grayscale frame
        # rects = detector.detectMultiScale(
        #     cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), scaleFactor=1.1, 
        #     minNeighbors=5, minSize=(30, 30))

        # # loop over the face detections and draw them on the frame
        # for (x, y, w, h) in rects:
        #     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # show the output frame
        flipped = cv2.flip(frame, 1)
        img_final = cv2.cvtColor(flipped, cv2.COLOR_BGR2RGB)
        frameST.image(img_final)


if selection != "only camera": 
    st.write("selexionato due")

    @st.cache(allow_output_mutation=True)
    def get_cap():
        return cv2.VideoCapture(0)

    cap = get_cap()

    frameST = st.empty()

    # loop over the frames from the video stream
    while True:
        ret, frame = cap.read()

        # # detect faces in the grayscale frame
        # rects = detector.detectMultiScale(
        #     cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), scaleFactor=1.1, 
        #     minNeighbors=5, minSize=(30, 30))

        # # loop over the face detections and draw them on the frame
        # for (x, y, w, h) in rects:
        #     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # show the output frame
        flipped = cv2.flip(frame, 1)
        img_final = cv2.cvtColor(flipped, cv2.COLOR_BGR2RGB)
        frameST.image(img_final)


        #Convert captured image to JPG
        retval, buffer = cv2.imencode('.jpg', img_final)
        # Convert to base64 encoding 
        base64str = base64.b64encode(buffer)

        url = "http://localhost:8000/send_frame_from_string/stream002" 
        
        payload = json.dumps({"img_base64str": base64str}, cls=BytesEncoder)
        response = requests.post(url,data = payload)
        #print(payload) 