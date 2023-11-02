import threading
import cv2
from datetime import datetime
from PIL import Image, ImageDraw, ImageOps

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
    print("Captuaring ENDED !")
  
  def join(self):
     """Call for the parent threadd to wait for camera thread"""
     if self.camera_thread.is_alive(): self.camera_thread.join()

class ImageUtils:
   def __init__(self):
       
      pass
   @staticmethod
   def create_rounded_image(frame) -> Image:
      """Create a rounded image from a frame"""
      frame = Image.fromarray(frame)
      size = frame.size[0] if frame.size[0] < frame.size[1] else frame.size[1]
      mask = Image.new('L',(size,size) , 1)
      draw = ImageDraw.Draw(mask) 
      draw.ellipse((0, 0) + mask.size, fill=255)
      output = ImageOps.fit(frame, mask.size, centering=(0.5, 0.5))
      output.putalpha(mask)
      return output
   @staticmethod
   def resize_image(image:Image,new_size:tuple[int,int]) -> Image:
      return image.resize((new_size))
