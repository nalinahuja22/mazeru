# Developed by matthew-notaro, nalinahuja22, and ClarkChan1

import os
import random

from audio import Audio
from video import Video
from moviepy.editor import *

# End Imports----------------------------------------------------------------------------------------------------------------------------------------------------------

MIN_CUT_THRESHOLD = 1
MAX_CUT_THRESHOLD = 31

# End Constants--------------------------------------------------------------------------------------------------------------------------------------------------------

class Timeline:
    def __init__(self, a_path, v_path, o_path):
        # Initialize Media Paths
        self.a_path = a_path
        self.v_path = v_path
        self.o_path = o_path

        # declare video and audio objects
        self.audio_obj = None
        self.video_obj = None

        # Initialize Cut Thresholds
        self.min_cthr = MIN_CUT_THRESHOLD
        self.max_cthr = MAX_CUT_THRESHOLD

        # Load Media
        self.load_media()

        # Process Media
        self.process_media()

    def load_media(self):
        # Load Audio Media
        self.audio_obj = Audio(self.a_path)

        # Load Video Media
        self.video_obj = random.shuffle([Video(file) for file in (os.listdir(self.v_path))])

    def process_media(self):
        # Process Audio Media
        (self.audio_obj).analyze()

        # Process Video Media
        for obj in (self.video_obj):
            (obj).analyze()

    def render(self):
        # Clip Sequence
        seq = []

        # Sequence Parameters
        lpeak = 0

        # Iterate Over Audio Peaks
        for peak in enumerate(self.audio_obj.peaks):
            # Compute Time Values
            t_end = peak // self.audio_obj.sample_rate
            t_start = lpeak // self.audio_obj.sample_rate
            t_delta = (t_end - t_start)

            # Verify Clip Duration
            if (t_delta < self.min_cthr):
                continue

            # Video Object
            video_clip = self.video_obj.pop(0)

            # Ensure Clips Exist
            if (not(video_clip)):
                break
            elif (t_delta > video_clip.get_duration()):
                # Iterate Over Remaining Clips
                for i in range(1, len(self.video_obj)):
                    # Optimize Video Clip
                    if (t_delta <= self.video_obj[i].get_duration()):
                        video_clip = self.video_obj[i]
                        break

            # Append Trimmed Clip To Sequence
            seq.append(video_clip.cut(0, t_delta))

            # Update Parameters
            lpeak = peak

        # Render Video
        seq = concatenate_videoclips(seq)
        seq.write_videofile(self.o_path)

# End Classes----------------------------------------------------------------------------------------------------------------------------------------------------------
