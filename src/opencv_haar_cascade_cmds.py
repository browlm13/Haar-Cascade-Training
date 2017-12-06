#!/usr/bin/env python

# internal
import logging
import os
import glob

# external
import cv2

"""
	Opencv Haar Cascade commands
"""

#NOTE: opencv_createsamples img -info positive_basketballs.txt -vec ../vector_files/positive_basketballs.vec -w 20 -h 20 -num 500
#		Must be run from same directory as info file

def create_vector_file(sample_settings):
	size = 3000	#not sure what to do about this

	#
	# read positive sample settings
	#

	width = sample_settings['POSITIVE_SAMPLES']['Sample Image Width']
	height = sample_settings['POSITIVE_SAMPLES']['Sample Image Height']

	info_files = glob.glob('data/working_data/info_files/*')
	positive_info_file_dataset_names = []
	for f in info_files:
		basename = os.path.basename(f)
		set_type = basename.split('_')[0]
		if set_type == 'positive':
			dataset_name = basename.split('.')[0]
			positive_info_file_dataset_names.append(dataset_name)

	#
	# change current working directory to info file directory
	#
	#cmds must be run in info file directory
	info_file_directoy = glob.glob('data/working_data/info_files')[0]

	#change to info files dir
	os.chdir(info_file_directoy)
	#os.getcwd()


	#cmd = 'opencv_createsamples img -info positive_basketballs.txt -vec ../vector_files/positive_basketballs.vec -w 20 -h 20 -num 500'

	#
	# run command to generate positive vector files
	#
	for dsn in positive_info_file_dataset_names:
		# find number of image files for each dataset (size)
		glob_template = '../generated_samples/%s/*' % dsn
		size = len(glob.glob(glob_template))

		template_cmd = 'opencv_createsamples img -info %s.txt -vec ../vector_files/%s.vec -w %d -h %d -num %d'
		cmd = template_cmd % (dsn, dsn, width, height, size)
		os.system(cmd)

def train_cascades(sample_settings):
	#opencv_traincascade -data ../cascades -vec ../vector_files/positive_basketballs.vec -bg negitive_backgrounds.txt -numPos 500 -numNeg 500 -numStages 5 -w 20 -h 20
	#currently only option is to use default negitive_backgrounds.txt
	template_cmd = 'opencv_traincascade -data ../cascades -vec ../vector_files/%s.vec -bg negitive_backgrounds.txt -numPos 500 -numNeg 500 -numStages 5 -w 20 -h 20'
	#negitive h,w have to be same as positive
	pass

