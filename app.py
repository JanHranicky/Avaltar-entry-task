from flask import Flask, render_template, Response, send_file, request, send_from_directory
from time import time
import time 
from services.camera import Camera
from config import Config
import torch 
import os
import os
import re

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

def get_chunk(filename, byte1=None, byte2=None):
    filesize = os.path.getsize(filename)
    yielded = 0
    yield_size = 256

    if byte1 is not None:
        if not byte2:
            byte2 = filesize
        yielded = byte1
        filesize = byte2

    with open(filename, 'rb') as f:
        content = f.read()

    while True:
        remaining = filesize - yielded
        if yielded == filesize:
            yielded = 0
        if remaining >= yield_size:
            yield content[yielded:yielded+yield_size]
            yielded += yield_size
        else:
            yield content[yielded:yielded+remaining]
            yielded += remaining

@app.route('/video_feed')
def video_feed():
    filename = './static/video1.mp4'
    filesize = os.path.getsize(filename)
    range_header = request.headers.get('Range', None)

    if range_header:
        byte1, byte2 = None, None
        match = re.search(r'(\d+)-(\d*)', range_header)
        groups = match.groups()

        if groups[0]:
            byte1 = int(groups[0])
        if groups[1]:
            byte2 = int(groups[1])

        if not byte2:
            byte2 = byte1 + 1024 * 1024
            if byte2 > filesize:
                byte2 = filesize

        length = byte2 + 1 - byte1

        resp = Response(
            get_chunk(filename, byte1, byte2),
            status=206, mimetype='video/mp4',
            content_type='video/mp4',
            direct_passthrough=True
        )

        resp.headers.add('Content-Range',
                         'bytes {0}-{1}/{2}'
                         .format(byte1,
                                 length,
                                 filesize))
        return resp

    return Response(
        get_chunk(filename),
        status=200, mimetype='video/mp4'
    )
    
@app.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response


if __name__ == '__main__':
    app.config.from_object(Config())
    app.run(debug=True,threaded=True)
    
    
    