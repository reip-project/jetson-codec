import os
import subprocess
import shlex

def return_gstreamer_string_old(infile, width, height, fps, bitrate_kbs, outfname, file_length_seconds):
	print(os.path.join(tmp_out_path, outfname))
	gstr = 	'gst-launch-1.0 filesrc location=%s ! ' \
			'"image/jpeg, width=%d, height=%d, framerate=%d/1" ! ' \
			'jpegdec ! ' \
			'nvvidconv ! ' \
			'"video/x-raw(memory:NVMM), format=(string)I420" ! ' \
			'omxh264enc iframeinterval=1 bitrate=%d ! ' \
			'"video/x-h264, stream-format=(string)byte-stream" ! ' \
			'h264parse ! ' \
			'splitmuxsink location=%s/out_%%d.mp4 max-size-time=%d' \
			% (infile, width, height, fps, bitrate_kbs * 1024, os.path.join(tmp_out_path, outfname), file_length_seconds * 1000000000)
	return gstr

def return_gstreamer_string(infile, bitrate_kbs, outpath):

	gstr = 	'gst-launch-1.0 filesrc location=%s ! ' \
			'qtdemux ! ' \
			'queue ! ' \
			'h264parse ! ' \
			'omxh264dec ! ' \
			'omxh264enc bitrate=%d ! ' \
			'"video/x-h264, stream-format=(string)byte-stream" ! ' \
			'h264parse ! ' \
			'qtmux ! ' \
			'filesink location=%s/out_%dkbps.mp4 -e' \
			% (infile, bitrate_kbs * 1024, outpath, bitrate_kbs)
	print(gstr)
	return gstr


input_file = 'demo_video/demo.mp4'
bitrate = 200
output_root_path = 'output_video'

gstr = return_gstreamer_string(input_file, bitrate, output_root_path)
record_proc = subprocess.Popen(shlex.split(gstr), stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
outs, errs = record_proc.communicate()
print('Error: %s' % str(errs))
print('Outputs: %s' % str(outs))