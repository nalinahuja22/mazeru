# Developed by matthew-notaro, nalinahuja22, and ClarkChan1
from audio import Audio

class Cut:
    def __init__(self, vfile, itime, otime):
        self.vfile = vfile
        self.itime = itime
        self.otime = otime

class Timeline:
    def __init__(self, a_path, v_path):
        self.a_path = v_path
        self.v_path = v_path

        self.a_obj = Audio(a_path)
        # self.v_obj = Video(v_path)

    def render(self):
        self.a_obj.analyze()
        print(len(self.a_obj.peaks))

obj = Timeline("../media/audio/sensation.wav", None)
obj.render()