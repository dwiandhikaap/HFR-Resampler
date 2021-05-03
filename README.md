# HFR-Resampler

HFR-Resampler is a tool to resample high framerate video into lower framerate video with customizable weighting.

## Example
![the example](https://i.imgur.com/6HEa2wd.gif)

yeah i know the difference between gaussian and pyramid is subtle, but it'll become adjustable in the future

## Usage
1. Download the latest release
2. Extract it
3. Copy the video into the same folder
4. Open your Command Line/Terminal on that directory, and then type `resampler.exe -h` to show the help (More details on this later)

Example
`resampler.exe -i input.mp4 -o input_resampled.mkv -fps 60 -m 6 -r 2.0 -res 1920x1080`
Will use "input.mp4" as input, and will output "input_resampled.mkv" on 1920x1080 resolution on 60 FPS. Which used my own Weighting Preset as the Weighting Method (`-m 6` , more details on this later), and resampled on 2.0 blend range (Check the definition of Blend Range in the help menu)

## License
[MIT](https://choosealicense.com/licenses/mit/)
