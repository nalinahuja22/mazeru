# Developed by matthew-notaro, nalinahuja22, and ClarkChan1

import argparse

from timeline import Timeline

# End Imports----------------------------------------------------------------------------------------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("audio_path", help="path to audio file")
    parser.add_argument("video_path", help="path to directory that contains videos")
    parser.add_argument("output_path", help="path to where the output file will be stored")
    parser.add_argument("min_seconds", help="minimum threshold time interval to cut", type=int, nargs='?')
    parser.add_argument("max_seconds", help="maximum threshold time interval to cut", type=int, nargs='?')
    args = parser.parse_args()


    vid_maker = Timeline(args.audio_path, args.video_path)

    if args.min_seconds:
        vid_maker.min_thr = args.min_seconds

    if args.max_seconds:
        vid_maker.max_thr = args.max_seconds

    vid_maker.render()

if __name__ == "__main__":
    main()

# End File-------------------------------------------------------------------------------------------------------------------------------------------------------------
