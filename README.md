## jetson-codec
deployment of video compression part on jetson nano platform using ffmpeg  

## install
The following code should be able to give you latest version [4.2.2](https://launchpad.net/ubuntu/+source/ffmpeg)  
`sudo apt-get update`  
`sudo apt-get install ffmpeg`  

Check version and configuration (some codec require extra --enable):
`ffmpeg -version`  

Previous ubuntu FFmpeg does not have some codec we need. Currently we are using a static build to produce some results. Follow this [post](https://www.johnvansickle.com/ffmpeg/faq/) to install. Also if you want to have different version of FFmpeg in one operating system you can check the way to execute them in this post.  
Our version check looks like this:  
```
ffmpeg version N-51578-g62d92a878d-static https://johnvansickle.com/ffmpeg/  Copyright (c) 2000-2020 the FFmpeg developers  
built with gcc 6.3.0 (Debian 6.3.0-18+deb9u1) 20170516  
configuration: --enable-gpl --enable-version3 --enable-static --disable-debug --disable-ffplay --disable-indev=sndio --disable-outdev=sndio --cc=gcc-6 --enable-fontconfig --enable-frei0r --enable-gnutls --enable-gmp --enable-libgme --enable-gray --enable-libaom --enable-libfribidi --enable-libass --enable-libvmaf --enable-libfreetype --enable-libmp3lame --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libopenjpeg --enable-librubberband --enable-libsoxr --enable-libspeex --enable-libsrt --enable-libvorbis --enable-libopus --enable-libtheora --enable-libvidstab --enable-libvo-amrwbenc --enable-libvpx --enable-libwebp --enable-libx264 --enable-libx265 --enable-libxml2 --enable-libdav1d --enable-libxvid --enable-libzvbi --enable-libzimg  
libavutil      56. 38.100 / 56. 38.100  
libavcodec     58. 67.100 / 58. 67.100  
libavformat    58. 37.100 / 58. 37.100  
libavdevice    58.  9.103 / 58.  9.103  
libavfilter     7. 72.100 /  7. 72.100  
libswscale      5.  6.100 /  5.  6.100  
libswresample   3.  6.100 /  3.  6.100  
libpostproc    55.  6.100 / 55.  6.100  
```

## Testing available codec
According the FFmpeg codec [documentation](https://www.ffmpeg.org/ffmpeg-codecs.html#mpeg2), they provide 20 video encoders. However some of them require additional `--enable [codec name]` during configuration, which I failed to find. The above FFmpeg is the most complete version I could find some online. Now we have tested the following six kind of codec. See the details in the `script` directory  
### libaom-av1
Check [here](https://trac.ffmpeg.org/wiki/Encode/AV1) for code format.  
Use option `-crf` to adjust the tradeoff between video quality and file size. Range: 0-63  
Lower values mean better quality and greater file size.  

### libvpx: VP8
Check [here](https://trac.ffmpeg.org/wiki/Encode/VP8) for code format.  
Use option `-crf` to adjust the tradeoff between video quality and file size. Range: 4-63  
10 is generally a good starting point. Lower values mean better quality.  

### libvpx: VP9
Check [here](https://trac.ffmpeg.org/wiki/Encode/VP9) for code format.  
In this codec we use Two-pass. IT is the recommended encoding method for libvpx-vp9 as some quality-enhancing encoder features are only available in 2-pass mode.
Use option `-crf` to adjust the tradeoff between video quality and file size. Range: 0-63  
Lower values mean better quality. Recommended values range from 15–35, with 31 being recommended for 1080p HD video.  

### libx264
Check [here](https://trac.ffmpeg.org/wiki/Encode/H.264) for code format.  
Use option `-crf` to adjust the tradeoff between video quality and file size. Range: 0-51  
>The range of the CRF scale is 0–51, where 0 is lossless, 23 is the default, and 51 is worst quality possible. A lower value generally leads to higher quality, and a subjectively sane range is 17–28. Consider 17 or 18 to be visually lossless or nearly so; it should look the same or nearly the same as the input but it isn't technically lossless. 
>The range is exponential, so increasing the CRF value +6 results in roughly half the bitrate / file size, while -6 leads to roughly twice the bitrate.
>Choose the highest CRF value that still provides an acceptable quality. If the output looks good, then try a higher value. If it looks bad, choose a lower value.

### libx265
Check [here](https://trac.ffmpeg.org/wiki/Encode/H.265) for code format.  
Use option `-crf` to adjust the tradeoff between video quality and file size. Range: 0-51  
The default is 28, and it should visually correspond to libx264 video at CRF 23, but result in about half the file size. Other than that, CRF works just like in x264.  

### libxvid
Check [here](https://trac.ffmpeg.org/wiki/Encode/MPEG-4) for code format.  
Use option `-qscale:v` to adjust the tradeoff between video quality and file size. Range: 1-31  
qscale = 1 being highest quality/largest filesize and 31 being the lowest quality/smallest filesize. This is a variable bit rate mode, roughly analogous to using -qp (constant QP [quantization parameter]) with x264. Most of the time this should be the preferred method.

## Current problems
Most of our FFmpeg codec here are running pretty slow. More work might need to be done to improve the speed. FFmpeg actually provides the option like setting up the desired bit rate to speed up the encoding, but this would cause some downgrade to the video quality.  
Also `-crf` is not necessary the only params to tune the output video. Might think about other options when we have better knowledge in the object detection process.
We can also consider the hardware encoders like VAAPI encoder in FFmpeg documentation. But I haven't figure out how to do that.

## Next steps
Build pipelines to perfrom object detection from our available sets of experiment outcomes. However currently there is no python package to perfrom pedestrain count. Need to revise some github repo. 
  







