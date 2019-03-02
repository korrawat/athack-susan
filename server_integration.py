from flask import Flask, render_template, Response, jsonify, request
from camera import VideoCamera
from camera import Camera
from image_processor import ProcessedStream
from processor_properties import ProcessorProperties
import cv2

app = Flask(__name__)

video_camera = None
global_frame = None

@app.route('/')
def index():
    return render_template('index.html')

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
    
    c = Camera(debug=True)
    p = ProcessorProperties() 
    pstream = ProcessedStream(c, p)
    
    p.brightness_factor.update(2)
        
    while True:
        #frame = video_camera.get_frame()
        #frame = c.snapshot_JPEG() 

        frame_original, frame_processed = pstream.read()
        ret, jpeg = cv2.imencode('.jpg', frame_processed)
        frame = jpeg.tobytes()
        if frame is not None:
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
