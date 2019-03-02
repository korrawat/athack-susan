from flask import Flask, render_template, Response, jsonify, request
import os
import datetime

from camera import VideoCamera
import cv2

app = Flask(__name__)

video_camera = None
global_frame = None
counter = 1

captured_img_dir = 'static/img'

@app.route('/')
def index():
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
        cv2.imwrite(os.path.join(captured_img_dir, 'capture' + str(datetime.datetime.now()) + '.jpg'), frame)

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

def video_stream():
    global video_camera 
    global global_frame

    if video_camera == None:
        video_camera = VideoCamera()
        
    while True:
        frame = video_camera.get_frame()

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

@app.route('/images_list')
def images_list():
    working_dir = os.getcwd()
    full_paths = [os.path.join(working_dir, captured_img_dir, image_file) \
        for image_file in os.listdir(captured_img_dir)]
    print full_paths
    return full_paths


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)