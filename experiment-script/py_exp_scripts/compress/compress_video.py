import os, glob
import subprocess
import shlex
from tqdm import tqdm


def return_gstreamer_string(infile, bitrate_kbs, outpath):

	gstr = 	'gst-launch-1.0 filesrc location=%s ! ' \
			'qtdemux ! ' \
			'queue ! ' \
			'h264parse ! ' \
			'nvv4l2decoder ! ' \
			'nvv4l2h264enc bitrate=%d ! ' \
			'h264parse ! ' \
			'qtmux ! ' \
			'filesink location=%s/%s_out_%dkbps.mp4 -e' \
			% (infile, bitrate_kbs * 1024, outpath, os.path.basename(infile), bitrate_kbs)
	print(gstr)
	return gstr


input_path = 'input_video'
st_bitrate = 14500
en_bitrate = 20
bitrate_jump = 200
output_root_path = 'output_video'

# print(list(range(st_bitrate, en_bitrate, -bitrate_jump)))
# print(len(list(range(st_bitrate, en_bitrate, -bitrate_jump))))


for input_file in glob.glob(input_path + '/*.mp4'):
	print(input_file)

	for comp_bitrate in tqdm(list(range(st_bitrate, en_bitrate, -bitrate_jump))):
		gstr = return_gstreamer_string(input_file, comp_bitrate, output_root_path)
		record_proc = subprocess.Popen(shlex.split(gstr), stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
		outs, errs = record_proc.communicate()
		print('Error: %s' % str(errs))
		print('Outputs: %s' % str(outs))

