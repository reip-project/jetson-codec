import os
import subprocess
import shlex


def return_gstreamer_string(infile, bitrate_kbs, outpath):

	gstr = 	'gst-launch-1.0 filesrc location=%s ! ' \
			'qtdemux ! ' \
			'queue ! ' \
			'h264parse ! ' \
			'omxh264dec ! ' \
			'omxh264enc bitrate=%d ! ' \
			'h264parse ! ' \
			'qtmux ! ' \
			'filesink location=%s/out_%dkbps.mp4 -e' \
			% (infile, bitrate_kbs * 1024, outpath, bitrate_kbs)
	print(gstr)
	return gstr


input_file = 'demo_video/demo.mp4'
bitrate = 2000
output_root_path = 'output_video'

gstr = return_gstreamer_string(input_file, bitrate, output_root_path)
record_proc = subprocess.Popen(shlex.split(gstr), stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
outs, errs = record_proc.communicate()
print('Error: %s' % str(errs))
print('Outputs: %s' % str(outs))