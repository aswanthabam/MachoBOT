from common import SharedCam
import threading
import time
from UI import Interface

exit_flag = threading.Event() # Exit flag for ending threads

def launch():
  print("Launching MachoBOT ...")
  cam = SharedCam(exit_flag)
  cam.start_capturing()
  interface = Interface()
  interface.show()
  time.sleep(1)
  interface.start_showing_camera_feed(cam)
  # interface.show_bottom_greet_image()
  interface.window_closed(end_task)
  interface.join()
  
def end_task():
  exit_flag.set()
  time.sleep(0.1)
if __name__ == '__main__':
  launch()