from common import SharedCam
import threading
import time
from UI import Interface
from face import Face
exit_flag = threading.Event() # Exit flag for ending threads

def launch():
  print("Launching MachoBOT ...")
  # initializes the shared cam
  cam = SharedCam(exit_flag)
  cam.start_capturing() # start captuing in a thread
  # initialize an interface
  interface = Interface()
  interface.show() # start the UI thread
  time.sleep(1) # wait for the UI to bind
  interface.show_bottom_greet_image() # show the bottom image
  interface.window_closed(end_task) # bind event handler for closed window
  # initialize a face identifier
  face = Face(cam,exit_flag) 
  face.start_face_recognition()
  interface.start_showing_camera_feed(face) # show the camera images
  interface.join() # wait for the UI Thread
  
def end_task():
  exit_flag.set()
  time.sleep(0.1)
if __name__ == '__main__':
  launch()