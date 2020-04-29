from os import system
import argparse
import numpy as np
import sys
import cv2
from tqdm import tqdm
import pickle
import os
import glob
import multiprocessing
from threading import Thread
from queue import Queue
import time

print('OpenCV version: %s' % cv2.__version__)

# From: https://www.pyimagesearch.com/2017/02/06/faster-video-file-fps-with-cv2-videocapture-and-opencv/
class FileVideoStream:
    def __init__(self, path, queueSize=128):
        # initialize the file video stream along with the boolean
        # used to indicate if the thread should be stopped or not
        self.stream = cv2.VideoCapture(path)
        self.stopped = False
        # initialize the queue used to store frames read from
        # the video file
        self.Q = Queue(maxsize=queueSize)

    def start(self):
        # start a thread to read frames from the file video stream
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        # keep looping infinitely
        while True:
            # if the thread indicator variable is set, stop the
            # thread
            if self.stopped:
                return
            # otherwise, ensure the queue has room in it
            if not self.Q.full():
                # read the next frame from the file
                (grabbed, frame) = self.stream.read()

                # frame = cv2.resize(frame, (300, 300), interpolation=cv2.INTER_AREA)
 
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

                cuda_img = jetson.utils.cudaFromNumpy(frame)
                # if the `grabbed` boolean is `False`, then we have
                # reached the end of the video file
                if not grabbed:
                    self.stop()
                    return
                # add the frame to the queue
                self.Q.put(cuda_img)

    def read(self):
        # return next frame in the queue
        return self.Q.get()

    def more(self):
        # return True if there are still frames in the queue
        return self.Q.qsize() > 0

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True

# file_path = '../output_video/port_0_1572451294.mp4_out_14500kbps.mp4'
# file_path = '../output_video/port_0_1572451294.mp4_out_14100kbps.mp4'

out_path = 'inf_out'

# pool = multiprocessing.Pool()
os.system('jetson_clocks')

use_yolo = True

threshold = 0.1

if use_yolo:
    import darknet
else:
    import jetson.inference
    import jetson.utils

if use_yolo:
    configPath = "darknet/cfg/yolov4.cfg"
    weightPath = "darknet/yolov4.weights"
    metaPath = "darknet/cfg/coco.data"
    netMain = darknet.load_net_custom(configPath.encode("ascii"), weightPath.encode("ascii"), 0, 1)  # batch size = 1
    metaMain = darknet.load_meta(metaPath.encode("ascii"))
    with open(metaPath) as metaFH:
            metaContents = metaFH.read()
            import re
            match = re.search("names *= *(.*)$", metaContents, re.IGNORECASE | re.MULTILINE)
            if match:
                result = match.group(1)
            else:
                result = None
                if os.path.exists(result):
                    with open(result) as namesFH:
                        namesList = namesFH.read().strip().split("\n")
                        altNames = [x.strip() for x in namesList]
    darknet_image = darknet.make_image(darknet.network_width(netMain), darknet.network_height(netMain), 3)
    size = (darknet.network_width(netMain), darknet.network_height(netMain))
else:
    with open('ssd_coco_labels.txt', 'r') as f:
        labels = f.readlines()
    net = jetson.inference.detectNet("ssd-mobilenet-v3", [""], threshold)


def runner(file_path):

    path_split = os.path.split(file_path)[-1].split('_')

    bitrate = int(path_split[-1].split('.')[0].replace('kbps', ''))
    
    vid_info = cv2.VideoCapture(file_path)
    
    total_frames = int(vid_info.get(cv2.CAP_PROP_FRAME_COUNT))

    print('Total frames: %i' % total_frames)

    video_file_width = int(vid_info.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_file_height = int(vid_info.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if use_yolo:
        video = cv2.VideoCapture(file_path)
        video.set(3, video_file_width)
        video.set(4, video_file_height)
    else:
        video = FileVideoStream(file_path).start()


    fps = int(vid_info.get(cv2.CAP_PROP_FPS))

    vid_info.release()

    print('Video dimensions: %i x %i' % (video_file_width, video_file_height))

    frame_detection_array = []

    frame_hop = 1000

    for frame_idx in tqdm(range(0, total_frames, frame_hop)):
        
        if use_yolo:
            video.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret_val, img = video.read()
            if not ret_val:
                continue
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, size, interpolation=cv2.INTER_LINEAR)
            darknet.copy_image_from_bytes(darknet_image, img.tobytes())

            prev_time = time.perf_counter()
            detections = darknet.detect_image(netMain, metaMain, darknet_image, thresh=threshold)
            detection_time = time.perf_counter() - prev_time
        else:
            img = video.read()

            prev_time = time.perf_counter()
            detections = net.Detect(img, video_file_width, video_file_height, "box,label,conf")
            detection_time = time.perf_counter() - prev_time

        if use_yolo:
            for detection in detections:
                detection_dict = {  'frame_idx': frame_idx,
                                    'class_str': detection[0].decode("utf-8"),
                                    'confidence': detection[1],
                                    'left_top_x': detection[2][0],
                                    'left_top_y': detection[2][1],
                                    'width': detection[2][2],
                                    'height': detection[2][3],
                                    'bitrate_kbps': bitrate,
                                    'total_frames': total_frames,
                                    'file_path': file_path,
                                    'fps': fps,
                                    'detection_time': detection_time
                                }
                frame_detection_array.append(detection_dict)
        else:
            for detection in detections:
                detection_dict = {  'frame_idx': frame_idx,
                                    'class_id': detection.ClassID,
                                    'class_str': labels[detection.ClassID],
                                    'confidence': detection.Confidence,
                                    'left': detection.Left,
                                    'top': detection.Top,
                                    'right': detection.Right,
                                    'bottom': detection.Bottom,
                                    'width': detection.Width,
                                    'height': detection.Height,
                                    'area': detection.Area,
                                    'center': detection.Center,
                                    'bitrate_kbps': bitrate,
                                    'total_frames': total_frames,
                                    'file_path': file_path,
                                    'fps': fps,
                                    'detection_time': detection_time
                                }
                frame_detection_array.append(detection_dict)
    sys.stdout.flush()
    pickle.dump(frame_detection_array, open(os.path.join(out_path, os.path.basename(file_path) + '.p'), 'wb'))

for fpath in tqdm(glob.glob('../output_video/port_1_1572451294/*.mp4')):
    # pool.apply_async(runner, args=(fpath,))
    runner(fpath)

# pool.close()
# pool.join()

    
