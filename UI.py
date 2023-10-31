from tkinter import *
from PIL import Image, ImageTk
import cv2
from common import SharedCam
import threading

class CameraFeed:
  window = None
  width = 0
  height = 0
  label = None

  def __init__(self,window,width,height):
    self.window = window
    self.width = width 
    self.height = height 
    
    self.label = Label(window)
    self.label.pack()
    self.label.place(x=300,y=100)
  def update_frame(self,frame):
    if frame is None:return
    photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
    print("Updateign photot")
    self.label.config(image=photo)
    self.label.photo = photo
    # self.label.after(10, update_camera_feed)

class Interface:
  window = None
  screen_width = 0
  screen_height = 0
  cam_frame = None
  def __init__(self):
    self.ui_thread = threading.Thread(target=self.run)
    self.ui_thread.daemon = True
    self.camera_update_thread = threading.Thread(target=self.camera_update_thread_run)
    self.camera_update_thread.daemon = True
    pass

  def camera_update_thread_run(self):
    while True:
      frame = self.cam_frame.get_frame()[0]
      print(frame)
      self.camera_feed.update_frame(frame)
  def start_showing_camera_feed(self,cam : SharedCam):
    self.cam_frame = cam
    self.camera_update_thread.start()

  def show_bottom_greet_image(self):
    image1 = Image.open("assets/images/195.jpg")

    image1 = image1.resize((self.screen_width, self.screen_height), Image.ADAPTIVE)

    test = ImageTk.PhotoImage(image1)
    label1 = Label(image=test)
    label1.image = test
    
    label1.place(relwidth=1,relheight=1)
  def run(self):
    self.window = Tk()
    self.screen_width = self.window.winfo_screenwidth()
    self.screen_height = self.window.winfo_screenheight()
    self.window.geometry(f"{self.screen_width}x{self.screen_height}")

    self.window.title("MachoBOT")
    self.camera_feed = CameraFeed(self.window,self.screen_width,self.screen_height)  

    B = Button(self.window, text ="Click")
    B.place(x=50,y=50)
    self.window.protocol("WM_DELETE_WINDOW", self.on_closed)
    self.window.mainloop()
  def on_closed(self):
    if self.window_closed_callback:
      self.window_closed_callback()
    self.window.destroy()
  def show(self):
    self.ui_thread.start()
  def window_closed(self,callback):
    self.window_closed_callback = callback
  def join(self):
     """Call for the parent threadd to wait for ui thread"""
     if self.ui_thread.is_alive(): self.ui_thread.join()
