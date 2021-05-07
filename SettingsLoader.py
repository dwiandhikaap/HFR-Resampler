import argparse
import json

def load():
    settingsJson = None
    with open("settings.json") as settings:
        settingsJson = json.load(settings)

    args_parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    args_parser.add_argument("-i", "--input_name", required=True, type=str, 
                             help="""Name of the input file with extension.\
                                \nExample : -i vaxei_godmode.mp4""")

    args_parser.add_argument("-o", "--output_name", required=True, type=str, 
                             help="""Name of the output file with extension.\
                                \nExample : -o resampled_video.mkv""")

    args_parser.add_argument("-fps", "--output_fps", type=int, default=settingsJson["framerate"],
                             help="""Framerate/FPS of the output file.\
                                \nExample : -fps 60""")

    args_parser.add_argument("-m", "--blend_mode", type=int, default=settingsJson["blend_mode"],
                             help="""Weighting mode.\
                                \nTODO : add more explanation on this""")

    args_parser.add_argument("-r", "--blend_range", type=float, default=settingsJson["blend_range"],
                             help="""Range or Blend Range is the number that you get from how many frames resampled divided by the ratio between input and output fps.\
                                \nTips : Use value between 1.0 - 2.0, above 3.5 will cause blurry effect. This will also impact resampling performance""")

    args_parser.add_argument("-res", "--resolution", type=str, default=settingsJson["resolution"],
                             help="""Resolution of the output video.\
                                \nExample : -res 1920x1080 , -res UNCHANGED""")

    args_parser.add_argument("-fourcc", "--fourcc_code", type=str, default=settingsJson["fourcc"],
                             help="""Choose what video codec you want to use by their respective FOURCC code\
                                \nExample : -fourcc MJPG""")

    args_parser.add_argument("-cvfix", "--cv_colourfix", action='store_true', default=settingsJson["cv_colourfix"],
                             help="""Enable this if you're resampling video produced by osr2mp4 or anything that uses default OpenCV video writer codec\
                                \nExample : -cvfix""") 

    args_parser.add_argument('--version', action='version', version='HFR-Resampler v0.3')
                     

    parsed_args = args_parser.parse_args()

    return {
        "input_name": parsed_args.input_name,
        "output_name": parsed_args.output_name,
        "output_fps": parsed_args.output_fps,
        "blend_mode": parsed_args.blend_mode,
        "blend_range": parsed_args.blend_range,
        "resolution": parsed_args.resolution,
        "fourcc" : parsed_args.fourcc_code,
        "cv_colourfix" : parsed_args.cv_colourfix
    }