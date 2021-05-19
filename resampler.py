import numpy as np
import time
import subprocess
import os
import ntpath

from cv2 import cv2 as cv

from SettingsLoader import loadSettings
from Exceptions import *
from Weights import *

def blend(imgs, weights):
    try:
        img = np.einsum("ijkl,i->jkl", imgs, weights)
        return img.astype(np.uint8)
    except ValueError:
        img = np.zeros(imgs.shape)
        return img

# To fix weird OpenCV colorspace, code by caffeine
def colourFix(input_name):
    filename = ntpath.basename(input_name)
    os.rename(f"{input_name}", f"to-fix_{filename}")
    command = f"ffmpeg -i to-fix_{input_name} -vcodec libx264 -preset ultrafast -crf 1 -vf colormatrix=bt601:bt709,eq=gamma_g=0.97 -c:a copy {input_name}"
    subprocess.call(command, shell=True)

def addAudio(input_name, output_name):
    command = f"ffmpeg -i no-audio_{output_name} -i {input_name} -map 0:v -map 1:a -c copy {output_name}"
    subprocess.call(command, shell=True)
    os.remove(f"no-audio_{output_name}")

# overengineered resolution string parsing
def parseResolution(in_res, out_res):
    if out_res == "UNCHANGED":
        return in_res

    try:
        res = out_res.split("x")
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

def processVideo(settings):
    input_name = settings["input_name"]

    if settings["cv_colourfix"]:
        colourFix(input_name)

    input_video = cv.VideoCapture(input_name)

    if input_video is None or not input_video.isOpened():
        raise VideoReadError()

    output_name = settings["output_name"]
    output_fps = settings["output_fps"]
    blend_mode = settings["blend_mode"]
    blend_range = float(settings["blend_range"])
    input_res = [int(input_video.get(cv.CAP_PROP_FRAME_WIDTH)),
                 int(input_video.get(cv.CAP_PROP_FRAME_HEIGHT))]
    output_res = parseResolution(input_res,settings["resolution"])
    input_fps = round(input_video.get(cv.CAP_PROP_FPS))
    output_fps = int(output_fps)
    fps_ratio = int(input_fps/output_fps)
    input_nframes = input_video.get(cv.CAP_PROP_FRAME_COUNT)
    output_nframes = int(input_nframes/fps_ratio)
    fourcc_code = settings["fourcc"]

    print(f"Input Res : {input_res}\nOutput Res : {output_res}")

    blended_nframes = int(blend_range*fps_ratio)
    weights = weight(blend_mode, blended_nframes)

    output_video = cv.VideoWriter(filename=f"no-audio_{output_name}", fourcc=cv.VideoWriter_fourcc(*fourcc_code),
                                  fps=int(output_fps), frameSize=(output_res[0], output_res[1]))

    needResize = False
    if input_res != output_res:
        needResize = True

    time_list = [0]*15

    imgs = []
    input_video.set(cv.CAP_PROP_POS_FRAMES, 0)

    # First iteration, load all frames needed
    for _ in range(0, blended_nframes):
        _, frame = input_video.read()
        if needResize:
            frame = cv.resize(frame, (output_res[0], output_res[1]))
        imgs.append(frame)

    output_video.write(blend(np.asarray(imgs), weights))
    del imgs[:fps_ratio]

    # Next iteration, load remaining unloaded frames
    for i in range(1, int(output_nframes)):
        timer_start = time.process_time()
        for _ in range(0, fps_ratio):
            _, frame = input_video.read()
            if needResize:
                frame = cv.resize(frame, (output_res[0], output_res[1]))
            imgs.append(frame)

        output_video.write(blend(np.asarray(imgs), weights))
        del imgs[:fps_ratio]

        elapsed_time = (time.process_time()-timer_start)
        time_list.pop(0)
        time_list.append(elapsed_time)
        avg_time = sum(time_list)/len(time_list)

        print("\nPerformance  :", '%.3f' % (avg_time),
              "seconds/frame -", '%.3f' % (1/avg_time), "FPS")
        print("Estimation   :", time.strftime('%H:%M:%S',
              time.gmtime(math.ceil(avg_time*int(output_nframes-i)))))
        print(f"Progress     : {i}/{output_nframes} - ",
              '%.3f' % (100*i/output_nframes), "%")
            
    output_video.release()
    input_video.release()
    addAudio(input_name, output_name)

    if settings["cv_colourfix"]:
        os.remove(input_name)
        os.rename(f"to-fix_{input_name}", f"{input_name}")
        
def main():
    settings = loadSettings()
    
    processVideo(settings)

if __name__ == "__main__":
    main()