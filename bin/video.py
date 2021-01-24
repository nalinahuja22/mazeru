# Developed by matthew-notaro, nalinahuja22, and ClarkChan1

import os
import sys
import cv2
import imagehash

from PIL import Image
from moviepy.editor import *

# End Imports----------------------------------------------------------------------------------------------------------------------------------------------------------

class Video:
    def __init__(self, file):
        # Video File Path
        self.file = file

        # Integer list contains frames after which there is a cut
        # Cut between frame 10 and 11, break_arr contains 10
        self.break_arr = []

        # Dynamic motion difference average of non-zero hash differences
        self.motion_avg = 0
    
    
    # Returns the subclip of video given starting and ending times
    def cut(self, i_time, o_time):
        return VideoFileClip(self.file).subclip(i_time, o_time)


    # Populates break_arr with frames at which the scene changes 
    def analyze(self):
        # Video Frame Stream
        vidObj = cv2.VideoCapture(self.file)

        # For motion_avg calcs
        avg_counter = 0
        avg_sum = 0

        # Counter variable
        count = 0

        # Checks if frames were extracted
        success = 1

        # Extracts 1st frame
        success, image = vidObj.read()

        # Frame extractor loop
        while success:
            # Saves frame with frame-count
            cv2.imwrite("../media/frames/frame%d.jpg" % count, image)
            count += 1

            # Compares previous 2 frames
            if count >= 2:
                # Gets image hashes for last 2 frames
                hash0 = imagehash.average_hash(Image.open("../media/frames/frame%d.jpg" % (count - 2)))
                hash1 = imagehash.average_hash(Image.open("../media/frames/frame%d.jpg" % (count - 1)))

                # Calculates % difference 
                hash_diff = hash0 - hash1

                # Ensure Nonzero Hashdiff
                if hash_diff >= 1:

                    # Updates avg_counter and avg_sum and calculates new motion_avg
                    avg_counter = avg_counter + 1
                    avg_sum = avg_sum + hash_diff
                    self.motion_avg = avg_sum / avg_counter

                    # Compares to current motion average
                    if hash_diff >= self.motion_avg + 15:
                        self.break_arr.append(count - 2)

                    # Deletes previous frame so no more than 2 frames are saved at a time
                    os.remove("../media/frames/frame%d.jpg" % (count - 2))

            # Extracts next frame
            success, image = vidObj.read()

# End Class------------------------------------------------------------------------------------------------------------------------------------------------------------