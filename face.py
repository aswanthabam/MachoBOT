import cv2
from voice import Voice
from datetime import datetime
from common import SharedCam
import threading

class Face(SharedCam):
	cam = None
	exit_flag = None
	voice = None
	marked_face_image = None
	FACE_FOUND_ON = FACE_GONE_ON = datetime.now()
	FACE_NOT_FOUND_TIME = FACE_FOUND_TIME = 0
	
	def __init__(self,cam: SharedCam,exit_flag):
		super().__init__(exit_flag)
		self.face_cascade = cv2.CascadeClassifier('assets/cascade/haarcascade_frontalface_default.xml') # face 
		self.eye_cascade = cv2.CascadeClassifier('assets/cascade/haarcascade_eye.xml') # eye
		self.face_thread = threading.Thread(target=self.run_face_recognition)
		self.face_thread.daemon = True
		self.cam = cam
		self.exit_flag = exit_flag
		self.voice = Voice()

	def start_face_recognition(self):
		self.face_thread.start()
	
	def run_face_recognition(self):
		while not self.exit_flag.is_set():
			img,time = self.cam.get_frame()
			if img is None:continue
			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
			if len(faces) > 0:
					# Face is found say message
				self.FACE_FOUND_ON = datetime.now()
				diff = self.FACE_FOUND_ON - self.FACE_GONE_ON
				self.FACE_FOUND_TIME = diff.total_seconds()
				print("Found a face for : ",self.FACE_FOUND_TIME,'s',end='\r')
				if self.FACE_NOT_FOUND_TIME > 5 and self.FACE_FOUND_TIME < 1:
					# Say message
					self.voice.say_message("Hi, Welcome I'm Macho BOT")
				else:
					# Do nothing the person is infront of camera for a while
					pass
			else:
				self.FACE_GONE_ON = datetime.now()
				diff = self.FACE_GONE_ON - self.FACE_FOUND_ON
				self.FACE_NOT_FOUND_TIME = diff.total_seconds()

				print("No face found for :",self.FACE_NOT_FOUND_TIME,'s',end='\r')
			for (x,y,w,h) in faces:
				# To draw a rectangle in a face
				cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
				roi_gray = gray[y:y+h, x:x+w]
				roi_color = img[y:y+h, x:x+w]
				# Detects eyes of different sizes in the input image
				eyes = self.eye_cascade.detectMultiScale(roi_gray)

				# To draw a rectangle in eyes
				for (ex,ey,ew,eh) in eyes:
					cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,127,255),2)
			
			self.marked_face_image = img

	def get_frame(self) -> tuple :
		if self.marked_face_image is None:return None,None
		else: return self.marked_face_image,None