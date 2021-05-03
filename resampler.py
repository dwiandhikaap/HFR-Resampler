import argparse
import numpy as np
import time
import subprocess
import os
from cv2 import cv2 as cv

from Exceptions import *
from Weights import *

def addAudio(input_name, output_name):
    command = f"ffmpeg -i no-audio_{output_name} -i {input_name} -map 0:v -map 1:a -c copy {output_name}"
    subprocess.call(command, shell=True)
    os.remove(f"no-audio_{output_name}")

#overengineered resolution parsing
def parseResolution(resolution):
    try:
        res = resolution.split("x")
    except:
        raise InvalidResolution()

    new_res = []
    for value in res:
        try:
            new_res.append(int(value))
        except ValueError:
            raise InvalidResolution()

    if(len(new_res) != 2):
        raise InvalidResolution()
    else:
        return new_res

def processVideo(args):
    input_name      = args["input_name"]
    input_video     = cv.VideoCapture(input_name)

    if input_video is None or not input_video.isOpened():
       raise VideoReadError()

    output_name     = args["output_name"]
    output_fps      = args["output_fps"]
    blend_mode      = args["blend_mode"]
    blend_range     = float(args["blend_range"])
    output_res      = parseResolution(args["resolution"])
    input_res       = [int(input_video.get(cv.CAP_PROP_FRAME_WIDTH)), int(input_video.get(cv.CAP_PROP_FRAME_HEIGHT))]
    input_fps       = round(input_video.get(cv.CAP_PROP_FPS))
    output_fps      = int(output_fps)
    fps_ratio       = int(input_fps/output_fps)
    input_nframes   = input_video.get(cv.CAP_PROP_FRAME_COUNT)
    output_nframes  = int(input_nframes/fps_ratio)

    blended_nframes = int(blend_range*fps_ratio)
    weights = weight(blend_mode,blended_nframes)

    output_video = cv.VideoWriter(filename=f"no-audio_{output_name}",fourcc=cv.VideoWriter_fourcc(*"FFV1"), fps=int(output_fps), frameSize=(output_res[0], output_res[1]))

    needResize = False
    if input_res != output_res:
        needResize = True
    
    time_list = [0]*15

    imgs = []
    range1 = 0
    range2 = range1 + blended_nframes
    input_video.set(cv.CAP_PROP_POS_FRAMES, 0)

    for i in range(1, int(output_nframes)):
        timer_start = time.process_time()
        for _ in range(range1, range2):
            _, frame = input_video.read()
            if needResize:
                frame = cv.resize(frame, (output_res[0], output_res[1]))
            imgs.append(frame)

        output_video.write(blend(np.asarray(imgs),weights))
        del imgs[:fps_ratio]
        
        range1 = (i-1)*fps_ratio+blended_nframes
        range2 = (i)*fps_ratio+blended_nframes

        elapsed_time = (time.process_time()-timer_start)
        time_list.pop(0)
        time_list.append(elapsed_time)
        avg_time = sum(time_list)/len(time_list)
        
        print("\nPerformance  :", '%.3f'%(avg_time), "seconds/frame -", '%.3f'%(1/avg_time), "FPS")
        print("Estimation   :", time.strftime('%H:%M:%S', time.gmtime(math.ceil(avg_time*int(output_nframes-i)))))
        print(f"Progress     : {i}/{output_nframes} - ", '%.3f'%(100*i/output_nframes),"%")
    
    output_video.release()
    input_video.release()
    addAudio(input_name,output_name)

def blend(imgs, weights):
    P = np.einsum("ijkl,i->jkl", imgs, weights)
    return P.astype(np.uint8)

def main():
    args_parser = argparse.ArgumentParser()

    args_parser.add_argument("-i", "--input_name", help="Name of the input file with extension. Example : -i vaxei_godmode.mp4", type=str)
    args_parser.add_argument("-o", "--output_name", help="Name of the output file with extension.   Example : -o resampled_video.mkv", type=str)
    args_parser.add_argument("-fps", "--output_fps", help="Framerate/FPS of the output file.    Example : -fps 60", type=int)
    args_parser.add_argument("-m", "--blend_mode", help="Weighting mode.    TODO : add more explanation on this", type=int)
    args_parser.add_argument("-r", "--blend_range", help="Range or Blend Range is the number that you get from how many frames resampled divided by the ratio between input and output fps.     Tips : Use value between 1.0 - 2.5, above 3.5 will cause blurry video. This will also impact resampling performance", type=float)
    args_parser.add_argument("-res", "--resolution", help="Resolution of the output video.  Example : -res 1920x1080", type=str)

    parsed_args = args_parser.parse_args()

    args = {
        "input_name"  : parsed_args.input_name,
        "output_name" : parsed_args.output_name,
        "output_fps"  : parsed_args.output_fps,
        "blend_mode"  : parsed_args.blend_mode,
        "blend_range" : parsed_args.blend_range,
        "resolution"  : parsed_args.resolution,
    }

    processVideo(args)


if __name__ == "__main__":
    main()
    #titip : python resampler.py -i asd.mp4 -o asd_resampled.mp4 -fps 60 -res 1920x1080 -m 6