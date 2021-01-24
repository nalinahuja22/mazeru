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

        self.beat_timestamps = None

    def render(self):
        self.beat_timestamps = self.a_obj.get_beat_timestamps(0, self.a_obj.get_audio_duration())
        # self.beat_timestamps = self.a_obj.get_beat_timestamps(3, 5)
        print(len(self.beat_timestamps))

obj = Timeline("../media/audio/sensation.wav", None)
obj.render()