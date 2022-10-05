from fastapi import FastAPI, File, UploadFile,Request
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
import uvicorn
from fastapi_frame_stream import FrameStreamer
import base64
import sys
import cv2

sys.path.append("./")

app = FastAPI()
fs = FrameStreamer()

class InputImg(BaseModel):
    img_base64str : str

templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/camera")
def home(request: Request):
    return templates.TemplateResponse("camera.html", {"request": request})

############################################################################
## str64 GENERATION inside api
############################################################################
@app.post("/predict_str64", status_code=200)
async def predict_str64(file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return "Image must be jpg or png format!"
    base64str = base64.b64encode(await file.read()).decode("utf-8")
    return base64str


@app.post("/send_frame_from_file/{img_id}")
async def send_frame_from_file(img_id: str, file: UploadFile = File(...)):
    await fs.send_frame(img_id, file)


@app.post("/send_frame_from_string/{img_id}")
async def send_frame_from_string(img_id: str, d:InputImg):
    await fs.send_frame(img_id, d.img_base64str)


########################################################
              ## cascade 
##########################################################

app.post("/send_frame_from_string/{img_id}")
async def send_frame_from_string(img_id: str, d:InputImg):
    await fs.send_frame(img_id, d.img_base64str)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')



##########################################################
### for fendering a stream of base64 string
@app.get("/video_feed/{img_id}")
async def video_feed(img_id: str):
    return fs.get_stream(img_id)

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
