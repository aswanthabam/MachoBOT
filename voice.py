import gtts
from playsound import playsound

def say_message(msg):
  print("Saying msg : "+msg)
  t1 = gtts.gTTS(msg)
  t1.save("temp/pl.mp3")
  playsound("temp/pl.mp3")