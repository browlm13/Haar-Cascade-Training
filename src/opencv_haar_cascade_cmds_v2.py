#!/usr/bin/env python

# internal
import logging
import os
import glob
import json

# external
import cv2

# logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

"""
	Opencv Haar Cascade commands v2
"""

#NOTE: opencv_createsamples img -info positive_basketballs.txt -vec ../vector_files/positive_basketballs.vec -w 20 -h 20 -num 500
#		Must be run from same directory as info file

def create_vector_file(sample_settings):

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
	# 		(cmds must be run in info file directory)

	info_file_directoy = glob.glob('data/working_data/info_files')[0]
	os.chdir(info_file_directoy)

	#
	# run command to generate positive vector files
	#
	for dsn in positive_info_file_dataset_names:

		# find number of image files for each dataset (size)
		glob_template = '../generated_samples/%s/*' % dsn
		size = len(glob.glob(glob_template))

		# run command to create positive vector
		template_cmd = 'opencv_createsamples img -info %s.txt -vec ../vector_files/%s.vec -w %d -h %d -num %d'
		cmd = template_cmd % (dsn, dsn, width, height, size)
		os.system(cmd)

def train_cascades(model_name, positive_dataset_name, negitive_dataset_name, sample_settings, numPos, numStages):			#add model name parameter
	""" train cascade using passed settings and log settings to log file in model name directory, positive_dataset_name
		and negitive_dataset_name must contain the full directory names. """
	
	#
	# first switch to root directory
	#
	os.chdir('../haar_cascades')

	#
	# change current working directory to info file directory
	#	(cmds must be run in info file directory)

	info_file_directoy = glob.glob('data/working_data/info_files')[0]
	os.chdir(info_file_directoy)	# change current working directory to info files directory

	#
	# create new model directory
	#
	model_directory_path = '../cascades/' + model_name

	if not os.path.exists(model_directory_path):
		os.makedirs(model_directory_path)
	else: 
		logger.error('model with name %s already exists', model_name)
		return 0

	#
	# read positive sample settings
	#

	#negitive h,w have to be same as positive
	width = sample_settings['POSITIVE_SAMPLES']['Sample Image Width']
	height = sample_settings['POSITIVE_SAMPLES']['Sample Image Height']

	#
	# find numNeg as number of files in negitive dataset directory
	#

	glob_template = '../generated_samples/%s/*' % negitive_dataset_name
	numNeg = len(glob.glob(glob_template))

	#
	# write log file with model training settings
	#

	model_log_directory_path = model_directory_path + '/logs'		# create log directory inside new model directory
	model_log_file_path = model_log_directory_path + '/log.json'
	os.makedirs(model_log_directory_path)

	log_file_json = {
		'positive_dataset' : positive_dataset_name,
		'negitive_dataset' : negitive_dataset_name,
		'numPos' : numPos,
		'numNeg' : numNeg,
		'window_width' : width,
		'window_height' : height,
	}

	with open(model_log_file_path, 'w') as outfile:					# write json to file
		json.dump(log_file_json, outfile)

	#
	# train
	#

	# create cascade directory inside model directory
	model_cascade_directory_path = model_directory_path + '/cascade'
	os.makedirs(model_cascade_directory_path)

	# run training command
	template_cmd = 'opencv_traincascade -data %s -vec ../vector_files/%s.vec -bg %s.txt -numPos %d -numNeg %d -numStages %d -w %d -h %d'
	cmd = template_cmd % (model_cascade_directory_path, positive_dataset_name, negitive_dataset_name, numPos, numNeg, numStages, width, height)
	os.system(cmd)

