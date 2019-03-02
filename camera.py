import cv2
import threading
import glob
import os
import time
import numpy as np

class CameraFinder:
    def __iter__(self):
        self.i = -1
        return self

    def next(self):
        self.i += 1
        cap = cv2.VideoCapture(self.i)
        ret, frame = cap.read()
        cap.release()
        if ret:
            return self.i
        else:
            raise StopIteration

class Camera:
    def __init__(self, debug=False):
        self.debug = debug
        if not debug:
            self.cameraList = [i for i in CameraFinder()]
            assert len(self.cameraList) > 0, "No eligible cameras found!"
            #self.cap = cv2.VideoCapture(self.currentCamera)
            self.cap = None
            self.setCamera(0)
            print "Successfully found and opened camera."
        else:
            self.cameraList = [0, 1]
            self.currentCamera = 0
            self.debug_img_paths = glob.glob(os.path.join(os.path.abspath("."),'static','img','training_data','*'))
            self.debug_images = [cv2.imread(_) for _ in self.debug_img_paths]
            self.starttime = time.time()

    def setCamera(self, cameraIndex):
        self.currentCamera = cameraIndex
        if self.cap is not None:
            self.cap.release()
        self.cap = cv2.VideoCapture(self.currentCamera)

    def snapshot(self):
        if self.debug:
            timediff = int(np.floor(time.time() - self.starttime))
            # change image every 1 second:
            img_idx = timediff % len(self.debug_images)
            myimg = self.debug_images[img_idx]
            assert np.all(myimg <= 255) and np.all(myimg >= 0), "Values outside 0-255 detected in image"
            return myimg
        else:
            ret, frame = self.cap.read()
            return frame

    def snapshot_JPEG(self):
            frame = self.snapshot()
            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()


class RecordingThread (threading.Thread):
    def __init__(self, name, camera):
        threading.Thread.__init__(self)
        self.name = name
        self.isRunning = True

        self.cap = camera        
        width = int(self.cap.get(3))
        height = int(self.cap.get(4))
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.out = cv2.VideoWriter('./static/video.avi',fourcc, 20.0, (width, height))

    def run(self):
        while self.isRunning:
            ret, frame = self.cap.read()
            if ret:
                # frame = cv2.flip(frame,0)
                self.out.write(frame)

        self.out.release()

    def stop(self):
        self.isRunning = False

    def __del__(self):
        self.out.release()

class VideoCamera(object):
    def __init__(self):
        # Open a camera
        self.cap = cv2.VideoCapture(0)
      
        # Initialize video recording environment
        self.is_record = False
        self.out = None

        # Thread for recording
        self.recordingThread = None
    
    def __del__(self):
        self.cap.release()
    
    def get_frame(self):
        ret, frame = self.cap.read()

        if ret:
            ret, jpeg = cv2.imencode('.jpg', frame)

            # Record video
            # if self.is_record:
            #     if self.out == None:
            #         fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            #         self.out = cv2.VideoWriter('./static/video.avi',fourcc, 20.0, (640,480))
                
            #     ret, frame = self.cap.read()
            #     if ret:
            #         self.out.write(frame)
            # else:
            #     if self.out != None:
            #         self.out.release()
            #         self.out = None  

            return jpeg.tobytes()
      
        else:
            return None

    def start_record(self):
        self.is_record = True
        self.recordingThread = RecordingThread("Video Recording Thread", self.cap)
        self.recordingThread.start()

    def stop_record(self):
        self.is_record = False

        if self.recordingThread != None:
            self.recordingThread.stop()

            
