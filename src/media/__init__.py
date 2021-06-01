# Developed by Nalin Ahuja, nalinahuja22

import cli
import sys

from .audio import Audio, __process_audio
from .video import Video, __process_video

# End Imports------------------------------------------------------------------------------------------------------------------------------------------------------------

def process(*obj):
    # Determine Media Object Type
    if (isinstance(obj[0], Audio) and not(__process_audio(obj[0], obj[1], obj[2]))):
        # Show Audio Processing Error
        sys.exit(cli.nl(2) + "mazeru: Failed to process audio file, exiting...")
    elif (isinstance(obj[0], Video) and not(__process_video(obj[0]))):
        # Show Video Processing Error
        sys.exit(cli.nl(2) + "mazeru: Failed to process video file, exiting...")

# End Processing Wrapper Function----------------------------------------------------------------------------------------------------------------------------------------
