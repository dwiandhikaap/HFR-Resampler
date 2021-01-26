from cv2 import cv2 as cv
import os
import math
import numpy as np
import time

from Exceptions import OutputFpsNotValid
from Weights import *

#Processing the video from start to finish
def processVideo(input_name, output_fps, blend_mode, blend_range):
    time_elapsed = time.process_time()

    video = cv.VideoCapture(input_name)

    input_width = video.get(cv.CAP_PROP_FRAME_WIDTH)
    input_height = video.get(cv.CAP_PROP_FRAME_HEIGHT)
    input_fps = round(video.get(cv.CAP_PROP_FPS))

    try:
        output_fps = round(float(output_fps))
    except ValueError:
        raise OutputFpsNotValid()
 
    io_fps_ratio = int(input_fps/output_fps)

    input_nframes = video.get(cv.CAP_PROP_FRAME_COUNT)
    output_nframes = int(input_nframes/io_fps_ratio)

    #This is what the (blended_nframes/(input_fps/output_fps)) evaluates to
    #This will directly affect the motion blur effect, but also greatly affect the resampling time 
    #Minimum value is 1
    #blend_range = 3

    print("Input Resolution         : %ix%i" % (input_width,input_height))
    print("Input FPS                : %i" % input_fps)
    print("Output FPS               : %i" % output_fps)
    print("Input/Output FPS Ratio   : %i" % io_fps_ratio)
    print("Input Frame Count        : %i frames" % input_nframes)
    print("Output Frame Count       : %i frames" % output_nframes)
    print("Weighting Mode           : %s" % modeName(blend_mode))

    weights = weight(blend_mode,blend_range*io_fps_ratio)

    imgs = []
    first_frame = True
    last_frame_n = int(output_nframes)-blend_range
    for i in range(0, last_frame_n):
        timer1_start = time.process_time()

        if(first_frame):
            range1 = (i)*io_fps_ratio     
            range2 = (i+blend_range)*io_fps_ratio
            video.set(cv.CAP_PROP_POS_FRAMES, range1)
            first_frame = False

        else:
            range1 = (i+blend_range-1)*io_fps_ratio
            range2 = (i+blend_range)*io_fps_ratio
        
        for _ in range(range1, range2):
            _, frame = video.read()
            imgs.append(frame)

        final_image = blend(imgs,weights)

        del imgs[:io_fps_ratio]

        cv.imwrite("output/"+str(i)+".jpg", final_image)

        #Timing stuff
        spf = (time.process_time()-timer1_start)
        estimation = int((output_nframes-(i+1))*math.ceil(spf)) #Rounding up for worst case scenario i guess
        
        elapsed = int(time.process_time() - time_elapsed)

        print("\nProgress   : ", '%.3f'%(100*i/output_nframes), "percent")
        print("Performance  :", '%.3f'%(spf), "seconds/frame")
        print("Estimation   :", time.strftime('%H:%M:%S', time.gmtime(estimation)))
        print("Elapsed Time :", time.strftime('%H:%M:%S', time.gmtime(elapsed)))

#This code blends all the given frames with blending
def blend(imgs, weights):
    P = np.einsum("ijkl,i->jkl", imgs, weights)
    return P.astype(np.uint8)

def main():
    #todo, make a better temporary cli before implementing the gui, or don't (?) whatever

    os.system('cls' if os.name == 'nt' else 'clear')
    print("HighFrameRate Video Resampling Tool v0.1 by Siveroo")

    input_name = input("Enter the input file name with extension (Example: video.mp4)\n")
    os.system('cls' if os.name == 'nt' else 'clear')


    output_fps = input("Enter the desired video framerate (Example: 60)\n")
    os.system('cls' if os.name == 'nt' else 'clear')

    print("Input blending mode according it's numerical order!")
    for mode in Mode:
        print(modeName(mode))
    

    blend_mode = int(input("Input : "))-1
    os.system('cls' if os.name == 'nt' else 'clear')

    print("Input the blend range! (Minimum value is 1)") 
    print("\nInfo : The amount of blended input frames = (inputFps ÷ outputFps x blendRange).")
    print("       What i mean by blend range is that, how many frames do you")
    print("       want to blend into one frame, if the value is greater than 1")
    print("       it means that it will also include frames from the future and give")
    print("       really smooth transition between output frames")
    print("Warning : IT GREATLY INCREASES MEMORY USAGE AND PROCESSING TIME (LINEARLY?)\n")  

    blend_range = int(input("Input : "))
    os.system('cls' if os.name == 'nt' else 'clear')    

    #Multiprocessing will be implemented once i understand it well enough
    processVideo(input_name=input_name,output_fps=output_fps,blend_mode=blend_mode, blend_range=blend_range)

if __name__ == "__main__":
    main()
