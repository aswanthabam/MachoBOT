import threading
import cv2
import datetime

class SharedCam:
  frame = None
  time = None
  exit_flag = None
  last_captured = None
  
  def __init__(self,exit_flag):
    self.camera_thread = threading.Thread(target=self.run)
    self.camera_thread.daemon = True
    self.cap = cv2.VideoCapture(0)
    self.exit_flag  = exit_flag
  
  def get_frame(self):
     """Get the frame and the captured time"""
     return self.frame, self.last_captured
  
  def start_capturing(self,interval = 0):
    """ Start capturing : Start a thread"""
    self.camera_thread.start()
  
  def run(self):
    """Target function for the capture function to run"""
    print("CAPTURING")
    while not self.exit_flag.is_set():
        ret, frame = self.cap.read()
        if ret:
            self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.last_captured = datetime.now()
        cv2.imshow('img',self.frame)
        # Wait for Esc key to stop
        k = cv2.waitKey(30) & 0xff
        if k == 27:
          break
    print("Captuaring ENDED !")
  
  def join(self):
     """Call for the parent threadd to wait for camera thread"""
     if self.camera_thread.is_alive(): self.camera_thread.join()