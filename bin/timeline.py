# Developed by matthew-notaro, nalinahuja22, and ClarkChan1

import os

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
        self.video_obj = [Video(file) for file in (os.listdir(self.v_path))]

    def process_media(self):
        # Process Audio Media
        (self.audio_obj).analyze()

        # Process Video Media
        for obj in (self.video_obj):
            (obj).analyze()

    def render(self):
        seq = []

        lpeak = vindex = 0

        sr = self.audio_obj.sample_rate

        # Iterate Over Audio Peaks
        for peak in enumerate(self.audio_obj.peaks):
            # Ensure Clips Exist
            if (vindex < len(self.video_obj)):
                clip = self.video_obj[vindex]

                clip_end = peak // sr       # in seconds
                clip_start = lpeak // sr    # in seconds

                if ((clip_end - clip_start) > clip.duration):
                    clip_end = clip.duration + clip_start

                # Append Trimmed Clip To Sequence
                seq.append(clip.cut(clip_start, clip_end))

                # Update Parameters
                lpeak = peak
                vindex += 1

        # Render Video
        seq = concatenate_videoclips(seq)
        seq.write_videofile(self.o_path)

# End Classes----------------------------------------------------------------------------------------------------------------------------------------------------------
