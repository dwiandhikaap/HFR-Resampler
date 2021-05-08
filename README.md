# HFR-Resampler

HFR-Resampler is a tool to resample high framerate video into lower framerate video with customizable weighting.

## Example
![the example](https://i.imgur.com/6HEa2wd.gif)

yeah i know the difference between gaussian and pyramid is subtle, but it'll become adjustable in the future

## How to use
1. Download the latest release
2. Extract it
3. Copy the video into the same folder
4. Open your Command Line/Terminal on that directory, and then type `resampler.exe -h` to show the help, see more detailed explanation below.

**Video Tutorial**  
https://www.youtube.com/watch?v=fdra2CnEl1A

## Usage
You can use this program by running resampler.exe via terminal or cmd. Then, you can use the available arguments to customize the resampling process.

<b>Required Arguments</b>  
 - `-i INPUT_NAME`   : Specify the name of the input video file with   
   extension
   
 - `-o OUTPUT_NAME`  : Specify the name of the output video    file with
   extension

<b>Optional Arguments</b>  
 - `-h` : Show help menu provided by the program
 
 - `--version` : Show the version of the program
 - `-fps FPS` : Specify the framerate of the output video
 - `-r BLEND_RANGE` : Specify the Blend Range of the resampling process.
   It's the number you get from resampled **frame count** divided by
   **fps ratio of the input and output video**. Normal resampling is 1.0, but you can use 1.5, 2.0, or more, to resample more frames.
 - `-m BLEND_MODE` : Specify which blending mode to use. More details
   later below.
 - `-res WIDTHxHEIGHT` : Specify the resolution of the output video. Use
   `-res UNCHANGED` for no rescaling. This is also applicable in the
   `settings.json` file.
 - `-fourcc FOURCC_CODE` : Specify which video codec you want to use. Example : `-fourcc MPEG`
 - `-cvfix` : Enable colorfix ffmpeg script to fix the weird colorspace of the input video writen by OpenCV video writer.

<b>Blend Mode</b>  
Currently, the blend modes are still has to be specified by integers writen below.

 - Custom : 0 (***has not been implemented yet***)
 - Equal : 1
 - Gaussian : 2
 - Gaussian Symmetric : 3
 - Pyramid : 4
 - Pyramid Symmetric : 5
 - Siveroo's Preset : 6 (***will be replaced by custom weighting***)
 - Siveroo's Preset II : 7 (***will be replaced by custom weighting***)

**Output Filename Format**  
You should use video file format / video container that supports the codec you are using for the resampling process. For example, if you use FFV1 codec, you may want to use `.mkv` file format.

**Example**  
`resampler.exe -i input.mp4 -o input_resampled.mkv -fps 60 -m 6 -r 2.0 -res 1920x1080`
Will use "input.mp4" as input, and will output "input_resampled.mkv" on 1920x1080 resolution on 60 FPS. Which used my own Weighting Preset as the Weighting Method, and resampled on 2.0 blend range. 

## License
[![MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
