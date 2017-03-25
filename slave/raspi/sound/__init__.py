from subprocess import Popen
import time
class Manager:
    
    def __init__(self):
        self._filename2process = {}

    
    def play(self, filename):
        if filename in self._filename2process:
            self.stop(filename)
        args = ["cvlc", filename]
        self._filename2process[filename] = Popen(args)

    def stop(self, filename = None):
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
