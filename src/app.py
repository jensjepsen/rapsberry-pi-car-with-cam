import fastapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from PIL import Image

import base64
import io
from picamera2 import Picamera2
import libcamera

import models

from gpiozero import Robot, DistanceSensor

picam2 = Picamera2()
config = picam2.create_still_configuration(main={'size': (800, 600)})
config['transform'] = libcamera.Transform(vflip=1)
picam2.configure(config)

picam2.start()

robot = Robot(left=(17, 27), right=(24, 23))
distance = DistanceSensor(echo=5, trigger=6)

app = fastapi.FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
    allow_credentials=True,
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/')
def redirect():
    return RedirectResponse('/static/index.html')

@app.get('/img', response_model=models.StatusResponse)
def img():
    buffer = io.BytesIO()
    picam2.capture_file(buffer, format='jpeg')
    buffer.seek(0)

    img = Image.open(buffer)
    #img = img.resize(size=(400, 300))
    buffer_out = io.BytesIO()
    img.save(buffer_out, format='jpeg')
    buffer_out.seek(0)
    data = 'data:image/jpeg;base64,' + base64.b64encode(buffer_out.read()).decode('utf-8')

    print(distance.distance)
    return models.StatusResponse(distance=distance.distance, image=data)

@app.post('/act')
def act(action: models.ActionRequest):
    if act := getattr(robot, action.action):
        act()
