from flask import Flask, render_template, Response, jsonify, request, session
from flask_session import Session

import os
import datetime

from camera import VideoCamera, Camera
from image_processor import ProcessedStream
from processor_properties import ProcessorProperties

import cv2
from PIL import Image

app = Flask(__name__)

SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

video_camera = None
global_frame = None

@app.route('/')
def index():
    if not "bg" in session:
        session["bg"]=1
    if not "ct" in session:
        session["ct"] = 1
    if not "change" in session:
        session["change"] = False

    return render_template('landing.html')

@app.route('/capture_status', methods=['POST'])
def capture_status():
    global video_camera 
    if video_camera == None:
        video_camera = VideoCamera()
    json = request.get_json()

    status = json['status']

    if status == "true":
        frame = video_camera.get_image()
        cv2.imwrite(os.path.join('img', 'capture' + str(datetime.datetime.now()) + '.jpg'), frame)

    print('capture', status)

    return jsonify(result="captured")

@app.route('/record_status', methods=['POST'])
def record_status():
    global video_camera 
    if video_camera == None:
        video_camera = VideoCamera()

    json = request.get_json()

    status = json['status']

    if status == "true":
        video_camera.start_record()
        return jsonify(result="started")
    else:
        video_camera.stop_record()
        return jsonify(result="stopped")

@app.route('/tools', methods=['POST'])
def tools():
    global brightness
    global contrast
    global zoom

    global change

    json = request.get_json()

    bg = json['bg']
    ct = json['ct']
    zm = json['zm']

    # if bg:
    #     brightness = bg
    if ct:
        session["contrast"] = float(ct)
    # if zm:
    #     zoom = zm

    session["change"] = True

    print('change', session["change"])

    print('contrast', session["contrast"])

    return jsonify(result="changed")

def video_stream():
    global video_camera 
    global global_frame

    global change

    if video_camera == None:
        video_camera = VideoCamera()

    c = Camera()
    p = ProcessorProperties() 
    pstream = ProcessedStream(c, p)
    
    # p.brightness_factor.update(2)

    print('change', session["change"])

    if session["change"]:
        ct = session["contrast"]
        print(ct)
        p.contrast_factor.update(ct)
        # session["change"] = False
        
    while True:
        # frame = video_camera.get_frame()
        frame_original, frame_processed = pstream.read()
        ret, jpeg = cv2.imencode('.jpg', frame_processed)
        frame = jpeg.tobytes()

        if frame != None:
            global_frame = frame
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')

@app.route('/video_viewer')
def video_viewer():
    return Response(video_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)