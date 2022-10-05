from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Tuple
from fastapi.templating import Jinja2Templates
import uvicorn

class Faces(BaseModel):
    faces: List[Tuple[int, int, int, int]]

app = FastAPI()

@app.on_event("startup")
async def startup():
    cascade_classifier.load(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

cascade_classifier = cv2.CascadeClassifier()

@app.post("/predict")
async def predict(request: Request):
    request_body = await request.body()
    data = np.frombuffer(request_body, dtype=np.uint8)
    img = cv2.imdecode(data, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = cascade_classifier.detectMultiScale(gray)

    if len(faces) > 0:
        faces_output = Faces(faces=faces.tolist())
    else:
        faces_output = Faces(faces=[])
    print(faces_output)
    return faces_output.dict()


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

