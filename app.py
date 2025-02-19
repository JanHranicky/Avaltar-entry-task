from flask import Flask, render_template, Response
from time import time
import time 
from services.camera import Camera
from config import Config
import torch 

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    frame_interval = 1 / 30  # 30 FPS = 1/30 seconds per frame

    while True:
        frame = camera.get_frame()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        time.sleep(frame_interval) # sleep to simulate defined frame rate

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    
if __name__ == '__main__':
    app.config.from_object(Config())
    app.run(debug=True)
    
    
    