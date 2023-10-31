from tkinter import *
from PIL import Image, ImageTk
import cv2

class CameraFeed:
  window = None
  width = 0
  height = 0
  label = None
  def __init__(self,window,width,height):
    self.window = window
    self.width = width 
    self.height = height 
    
    self.label = window.Label(window)
    self.label.pack()
    
  def update_frame(self,ret,frame):
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        self.label.config(image=photo)
        self.label.photo = photo
    # self.label.after(10, update_camera_feed)

class Interface:
  window = None
  screen_width = 0
  screen_height = 0
  def __init__(self):
    self.window = Tk()
    self.screen_width = self.window.winfo_screenwidth()
    self.screen_height = self.window.winfo_screenheight()
    self.window.geometry(f"{self.screen_width}x{self.screen_height}")

    self.window.title("MachoBOT")
    
    image1 = Image.open("assets/images/195.jpg")

    image1 = image1.resize((self.screen_width, self.screen_height), Image.ADAPTIVE)

    test = ImageTk.PhotoImage(image1)
    label1 = Label(image=test)
    label1.image = test
    label1.place(relwidth=1,relheight=1)
    B = Button(self.window, text ="Click")
    B.place(x=50,y=50)
  
  def show(self):
    self.window.mainloop()


Interface().show()