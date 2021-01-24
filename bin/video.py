# Developed by matthew-notaro, nalinahuja22, and ClarkChan1

import os
import sys
from PIL import Image
import imagehash
import cv2

class Video:
    def __init__(self, file):
        self.file = file

        # Int list contains frames after which there is a cut
        # Cut between frame 10 and 11, break_arr contains 10
        self.break_arr = []

    def analyze(self, break_arr):
        vidObj = cv2.VideoCapture(file) 

        # Dynamic motion difference average
        motion_avg = 0

        # Counter variable 
        count = 0
        # Checks if frames were extracted 
        success = 1

        # Frame extractor loop
        while success: 
            # Extracts current frame 
            success, image = vidObj.read() 

            # Saves frame with frame-count 
            cv2.imwrite("frame%d.jpg" % count, image)
            count += 1

            # Compares previous 2 frames
            if count >= 2:
                # Gets image hashesf for last 2 frames
                hash0 = imagehash.average_hash(Image.open("frame%d.jpg" % count - 2)) 
                hash1 = imagehash.average_hash(Image.open("frame%d.jpg" % count - 1)) 
                
                # Calculates % difference and new motion_avg 
                hash_diff = hash0 - hash1
                motion_avg = ((motion_avg * (count-2)) + hash_diff) / (count-1)

                # Compares to current motion average
                if hash_diff <= motion_avg - 5: 
                    break_arr.append(count - 2)

                # Deletes previous frame so no more than 2 frames are saved at a time 
                os.remove("frame%d.jpg" % count - 2)

obj = Video("../media/video/soul.mp4")
obj.analyze(obj.break_arr)