# Developed by matthew-notaro, nalinahuja22, and ClarkChan1

import os
import subprocess

from audio import Audio
# from video import Video

# End Imports----------------------------------------------------------------------------------------------------------------------------------------------------------

class Cut:
    def __init__(self, file, i_time, o_time):
        self.file = file
        self.i_time = i_time
        self.o_time = o_time

class Timeline:
    def __init__(self, a_path, v_path):
        # Initialize Media Paths
        self.a_path = a_path
        self.v_path = v_path

        # declare video and audio objects
        self.audio_obj = None
        self.video_obj = None

        # Initialize Cut Thresholds

        self.min_thr = 1
        self.max_thr = 31


        # Load Media
        self.load_media()

        # Process Media
        self.process_media()

    def load_media(self):
        # Load Audio Media
        self.audio_obj = Audio(self.a_path)

        # Load Video Media
        # self.video_obj = [Video(file) for file in (os.listdir(self.v_path))]

    def process_media(self):
        # Process Audio Media
        (self.audio_obj).analyze()

        # Process Video Media
        for obj in (self.video_obj):
            (obj).analyze()

    def cut(self):
        

    def render(self):
        self.audio_obj.analyze()
        print(len(self.audio_obj.peaks))

# End Classes----------------------------------------------------------------------------------------------------------------------------------------------------------
