
import logging
import threading

from pydub import AudioSegment
from pydub.playback import play

logger = logging.getLogger("root")

name2filename = {"atmosphere":
                 "/home/pi/ZooMachine-3/slave/raspi/sound/atmosphere.mp3", 
                 "validation":
                 "/home/pi/ZooMachine-3/slave/raspi/sound/validation.mp3"
                 }

class Play(threading.Thread):
    def __init__(self, sound):
        super(Play, self).__init__()
        self.running = True
        self._sound = sound

    def run(self):
        play(self._sound)
        print("is end")
        self.running = False

    def stop(self):
        self.running = False

class Manager:

    def __init__(self):
        self._name2sound = {name: AudioSegment.from_mp3(filename) for 
                            name, filename in name2filename.items()}  
        self._name2process = {}

    def is_ended(self, name):
        if not self._is_avaible(name):
            return True
        if name not in self._name2process:
            return True

        return not self._name2process[name].is_alive()

    def restart_if_ended(self, name):
        if not self._is_avaible(name):
            return
        
        if self.is_ended(name):
            print("Process is ended")
            self.play(name)
        print("Process isn't ended")

    def play(self, name):
        if not self._is_avaible(name):
            return

        if name in self._name2process:
            self._name2process[name].stop()
        
        self._name2process[name] = Play(self._name2sound[name])
        self._name2process[name].start()

    def stop(self, name = None):
        if not name:
            #stop all
            for _, process in self._name2process.items():
                process.stop()

            self._name2process = {}
        else:
            if not self._is_avaible(name):
                return
            if name in self._name2process:
                self._name2process[name].stop()
                self._name2process.pop(name)

    def _is_avaible(self, name):
        if name not in self._name2sound:
            logger.error("Unknow sound name {} ".format(name))
            return False
        return True

if __name__ == "__main__":

    import time
    name2filename = {
        "atmosphere": "atmosphere.mp3",
        "validation": "validation.mp3"
    }
    m = Manager()

    # 4 repetition of validation separated by 1 second
    for _ in range(4):
        m.restart_if_ended("validation")
        time.sleep(1)

    # run atmosphere
    # 4 repetition of validation separated by 1 second
    # stop atmosphere
    m.play("atmosphere")
    for _ in range(4):
        m.restart_if_ended("validation")
        time.sleep(1)
    m.stop("atmosphere")

