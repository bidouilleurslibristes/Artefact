from subprocess import Popen
import time
import logging

logger = logging.getLogger("root")

class Manager:

    def __init__(self):
        self._filename2process = {}
        self._name2filename = {"atmosphere": "/home/pi/ZooMachine-3/slave/raspi/sound/atmosphere.mp3",
                               "validation": "/home/pi/ZooMachine-3/slave/raspi/sound/validation.mp3"
                               }

    def is_ended(self, name):
        if name not in self._name2filename:
            logger.error("Unknow sound name {} ".format(name))
            return True
        return self._filename2process[self._name2filename[name]].poll() is None

    def restart_if_ended(self, name):
        if self.is_ended(name):
            self.play(name)

    def play(self, name):
         if name not in self._name2filename:
            logger.error("Unknow sound name {} ".format(name))
            return
        self._play(self._name2filename[name])

    def _play(self, filename):
        if filename in self._filename2process:
            self._stop(filename)
        try:
            args = ["cvlc", "--play-and-exit", filename]
            self._filename2process[filename] = Popen(args)
        except Exception as e:
            logger.exception(e)

    def stop(self, name = None):
        if name not in self._name2filename:
            logger.error("Unknow sound name {} ".format(name))
            return
        self._stop(self._name2filename[name])

    def _stop(self, filename = None):
        if not filename:
            #stop all
            for _, process in self._filename2process.items():
                process.kill()

            self._filename2process = {}
        else:
            if filename in self._filename2process:
                self._filename2process[filename].kill()
                self._filename2process.pop(filename)

if __name__ == "__main__":
    m = Manager()
    m.play("sample.mp3")
    time.sleep(10)
    m.play("sample.mp3")
    time.sleep(10)
    m.stop()
