from flask import Flask, render_template, Response, send_file, make_response
from time import time
import time 
from services.camera import Camera

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hls-stream')
def hls_stream():
    return render_template('hls-stream.html')

@app.route('/hls_stream_feed/<filename>')
def hls_stream_feed(filename):
    print("here")
    response = make_response(send_file(
        './video/'+filename,
    ))
    response.headers["Content-Type"] = "application/x-mpegURL"
    return response

def gen(camera):
    frame_interval = 1 / 30  # 30 FPS = 1/30 seconds per frame

    while True:
        frame = camera.get_frame(encode_jpg=True)
              
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        time.sleep(frame_interval) # sleep to simulate defined frame rate

@app.route('/m-jpeg-stream')
def m_jpeg_stream():
    return render_template('m-jpeg-stream.html')

@app.route('/m_jpeg_stream_feed')
def m_jpeg_stream_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
        
if __name__ == '__main__':
    app.run(debug=True,threaded=True)
    
    
    