## jetson-codec
deployment of video compression part on jetson nano platform using ffmpeg

## install
Compared to the current master version of ffmpeg(3.x), the new released 4.0 "Wu" version has some new codec [available](ffmpeg.org/index.html#news).Especially:
> NVIDIA NVDEC-accelerated H.264, HEVC, MJPEG, MPEG-1/2/4, VC1, VP8/9 hwaccel decoding
which could be helpful for deployment on jetson nano.

Therefore, instead of regular apt-get install (which will get you version 3), we use:
`./install`
If encouter permission denied, use this before run the *install* script:
`sudo chmod 777 install`


