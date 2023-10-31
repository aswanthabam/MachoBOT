import cv2
import voice
from datetime import datetime
print("Starting Video Capture.. ")
cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier('res/haarcascade_frontalface_default.xml')

eye_cascade = cv2.CascadeClassifier('res/haarcascade_eye.xml')

# loop runs if capturing has been initialized.
FACE_FOUND_ON = FACE_GONE_ON = datetime.now()
FACE_NOT_FOUND_TIME = FACE_FOUND_TIME = 0
while 1:
	ret, img = cap.read()
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	if len(faces) > 0:
    	# Face is found say message
		FACE_FOUND_ON = datetime.now()
		diff = FACE_FOUND_ON - FACE_GONE_ON
		FACE_FOUND_TIME = diff.total_seconds()
		print("Found a face for : ",FACE_FOUND_TIME,'s')
		if FACE_NOT_FOUND_TIME > 5 and FACE_FOUND_TIME < 1:
			# Say message
			voice.say_message("Hi, Welcome I'm Macho BOT")
		else:
			# Do nothing the person is infront of camera for a while
			pass
	else:
		FACE_GONE_ON = datetime.now()
		diff = FACE_GONE_ON - FACE_FOUND_ON
		FACE_NOT_FOUND_TIME = diff.total_seconds()

		print("No face found for :",FACE_NOT_FOUND_TIME,'s')
	for (x,y,w,h) in faces:
		# To draw a rectangle in a face
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
		roi_gray = gray[y:y+h, x:x+w]
		roi_color = img[y:y+h, x:x+w]
		# Detects eyes of different sizes in the input image
		eyes = eye_cascade.detectMultiScale(roi_gray)

		# To draw a rectangle in eyes
		for (ex,ey,ew,eh) in eyes:
			cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,127,255),2)

	# Display an image in a window
	cv2.imshow('img',img)

	# Wait for Esc key to stop
	k = cv2.waitKey(30) & 0xff
	if k == 27:
		break

# Close the window
cap.release()

# De-allocate any associated memory usage
cv2.destroyAllWindows()

# gtts.gTTS("Hi, How are you?").save("temp/temp.mp3")
# playsound("temp/temp.mp3")