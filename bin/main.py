# Developed by matthew-notaro, nalinahuja22, and ClarkChan1
from timeline import Timeline
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("audio", help="path to audio file")
    parser.add_argument("video", help="path to directory that contains videos")
    parser.add_argument("--min_seconds", help="minimum threshold time interval to cut", type=int)
    parser.add_argument("--max_seconds", help="maximum threshold time interval to cut", type=int)
    args = parser.parse_args()

    if args.min_seconds:
        # set vid_maker.min_seconds to args.min_seconds
        pass
    if args.max_seconds:
        # set vid_maker.max_seconds to args.max_seconds
        pass

    vid_maker = Timeline(args.audio, args.video)
    vid_maker.render()

if __name__ == "__main__":
    main()