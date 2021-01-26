# HFR-Resampler

HFR-Resampler is a tool to resample high framerate video into lower framerate video with customizable weighting.

![the thumbnail](https://i.ibb.co/7RN8Dh3/shit-thumbnail.png)

## 🔧 Installation

This project requires ffmpeg, OpenCV and numpy installed. 

You can download ffmpeg [here](https://ffmpeg.org/download.html).

You can use [pip](https://pip.pypa.io/en/stable/) to install OpenCV and numpy.

```bash
pip install opencv-python
```

```bash
pip install numpy
```

## ✨ Usage

Currently it's still so complicated to do stuff with this, but for now here's how to use it :
1. install the dependecies
2. clone this stuff
3. move/copy your video input to the same directory as where the ```.py``` file is
4. make sure your video input is an ```.mp4``` format and named ```input.mp4```
5. run ```resample.py```
6. if it's working, it will output the resampled frames to the ```output``` folder
7. once it finished, you can reconstruct the video using ```ffmpeg```, you can google it if you don't know how to do it.
8. merge audio from original video and your resampled video together, you can use ```ffmpeg```. Again, google it if you don't know how.
9. yeah i think that's it, thank you for listening to my ted talk

## 👥 Contributing
currently still not accepting any external contribution since i haven't finished the important stuff yet, i'll update this page once it's ready


## 📄 License
[MIT](https://choosealicense.com/licenses/mit/)
