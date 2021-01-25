from cv2 import cv2 as cv
import math
import numpy as np
import time

# Some weighting function that spits out list/array/whatever it's called in python
def bell(n):
    r = range(n,0,-1)
    val = [math.exp(-(2*x/n)**2) for x in r]
    val = val/np.sum(val)
    return val

def bell_sym(n):
    n = int(n/2)
    r = range(n,-n,-1)
    val = [math.exp(-(1.5*x/n)**2) for x in r]
    val = val/np.sum(val)
    return val

#Processing the video from start to finish
def processVideo():
    time_elapsed = time.process_time()
    video = cv.VideoCapture("input.mp4")
    input_width = video.get(cv.CAP_PROP_FRAME_WIDTH)
    input_height = video.get(cv.CAP_PROP_FRAME_HEIGHT)

    input_fps = math.ceil(video.get(cv.CAP_PROP_FPS))
    output_fps = 60.0
 
    io_fps_ratio = int(input_fps/output_fps)

    input_nframes = video.get(cv.CAP_PROP_FRAME_COUNT)
    output_nframes = int(input_nframes/io_fps_ratio)

    #This is what the (blended_nframes/(input_fps/output_fps)) evaluates to
    #This will directly affect the motion blur effect
    #Minimum value is 1
    blend_range = 3

    print("Input Resolution         : %ix%i" % (input_width,input_height))
    print("Input FPS                : %i" % input_fps)
    print("Output FPS               : %i" % output_fps)
    print("Input/Output FPS Ratio   : %i" % io_fps_ratio)
    print("Input Frame Count        : %i frames" % input_nframes)
    print("Output Frame Count       : %i frames" % output_nframes)

    imgs = []
    first_frame = True
    for i in range(0, int(output_nframes)):
        timer1_start = time.process_time()

        if(first_frame):
            range1 = (i)*io_fps_ratio     
            range2 = (i+1)*io_fps_ratio
            video.set(cv.CAP_PROP_POS_FRAMES, range1)

        else:
            range1 = (i+blend_range-1)*io_fps_ratio
            range2 = (i+blend_range)*io_fps_ratio
        
        for _ in range(range1, range2):
            _, frame = video.read()
            imgs.append(frame)

        final_image = blend(imgs)

        del imgs[:io_fps_ratio]
        first_frame = False

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
def blend(imgs):
    num = len(imgs)
    Weight = bell_sym(num) #will be customizable
    P = np.einsum("ijkl,i->jkl", imgs, Weight)
    return P.astype(np.uint8)

def main():
    print("HighFrameRate Video Resampling Tool v0.1 by Siveroo")
    
    #Multiprocessing will be implemented once i understand it well enough
    processVideo()

if __name__ == "__main__":
    main()
