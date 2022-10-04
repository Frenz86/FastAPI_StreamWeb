import threading

import cv2
import streamlit as st
from matplotlib import pyplot as plt
import base64
from streamlit_webrtc import webrtc_streamer
import json
import requests

lock = threading.Lock()
img_container = {"img": None}

class BytesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode('utf-8')
        return json.JSONEncoder.default(self, obj)


def video_frame_callback(frame):
    img = cv2.flip(frame, 1)
    img = frame.to_ndarray(format="bgr24")
    with lock:
        img_container["img"] = img

    return frame

def main():
    ctx = webrtc_streamer(key="example", video_frame_callback=video_frame_callback)

    fig_place = st.empty()
    fig, ax = plt.subplots(1, 1)

    while ctx.state.playing:
        with lock:
            img = img_container["img"]
        if img is None:
            continue
        
        width = 200
        height = 140
        dim = (width, height)
        
        # resize image
        img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ax.cla()
        ax.hist(gray.ravel(), 256, [0, 256])
        fig_place.pyplot(fig)

        # # Convert captured image to JPG
        # retval, buffer = cv2.imencode('.jpg', img)
        # # Convert to base64 encoding 
        # base64str = base64.b64encode(buffer)

        # url = "http://localhost:8000/send_frame_from_string/stream002" 
        
        # payload = json.dumps({"img_base64str": base64str}, cls=BytesEncoder)
        # response = requests.post(url,data = payload)
        # print(payload) 


if __name__ == "__main__":
    main()