import gtts
from playsound import playsound
import threading
import os.path 

class Voice:
  msg = ""
  is_saying = False
  def __init__(self):
    pass
  def run_voice(self):
    self.is_saying = True
    print("Saying msg : "+self.msg)
    self.msg = self.msg.lower()
    path = f"generated/audio/{self.msg.replace(' ','')}.mp3"
    if os.path.isfile(path):
      playsound(path)
    else:
      t1 = gtts.gTTS(self.msg)
      t1.save(path)
      playsound(path)
    self.is_saying = False

  def say_message(self,msg):
    if self.is_saying:return False
    self.voice_thread = threading.Thread(target=self.run_voice)
    self.voice_thread.daemon = True
    self.msg = msg
    self.voice_thread.start()