# Thoughts on how to choose codec for this project

## ? Hardware acceleration on our chip: NVIDIA Jetson Nano

For Jetson Nano it has its own hardware encoder and decoder (not GPU). We should make use of the libraries that makes use of them. 
For some popular libraries like ffmpeg, it does not use these hardware. You may also use it but CPU-only.[Source](https://devtalk.nvidia.com/default/topic/1050950/jetson-nano/h-264-h-265-encoding-using-jetson-nano-gpu/)


NIVDIA actually suggesting using GStreamer and its plugin for video. Examples can be found [here](https://developer.download.nvidia.com/embedded/L4T/r32_Release_v1.0/Docs/Accelerated_GStreamer_User_Guide.pdf?xtzsWcFtZInDTqY5479b3PndhrGBId7fUrGAgZdsbqJYp89exmRsUT5H-HomaZbMJAcsAVnTTSu8labYz1DcXwuaQk1fAx_9eOv4DdTVrWV_r22gQOBCI4VxpbQf06NNe0qq4nQ_npVZ1o1-HPiaTdV-xUapurLNs82PeIrlC5dfBrsXed8). 

Note that in the above manual, *gst-omx* plugin is deprecated

So we use **gst-v412** plugin:
- Video Encoder:nvv4l2h264enc
- Description: V4l2 H.264 video encoder

- Video Encoder:nvv4l2h265enc 
- Description: V4l2 H.265 video encoder

- Video Encoder:nvv4l2vp8enc 
- Description: V4l2 VP8 video encoder (supported with Jetson Nano)

(There exists a video encoder in the manual:nvv4l2vp9enc, but it's not supported on Jetson Nano )

- Video Decoder: nvv4l2decoder
- Description: 
V4L2 H.265 Video decoder
V4L2 H.264 Video decoder
V4L2 VP8 video decoder
V4L2 VP9 video decoder
V4L2 MPEG4 video decoder
V4L2 MPEG2 video decoder

For this project, there is one NVIDIA plugins that might be helpful:
- nvvidconv: Video format conversion & scaling 
