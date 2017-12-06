#!/usr/bin/env python

# internal
import logging
import os
import glob

# my lib
from src import image_editing
from src import data_paths
from src import create_samples
from src import config_handler
from src import opencv_haar_cascade_cmds
from src import test_detection

# logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':

	#
	# config file
	#
	sample_settings = config_handler.sample_settings(data_paths.get_config_file_path())

	#
	# generate samples and info files for all raw image sets
	#
	#create_samples.generate_samples_for_all_raw_image_sets(sample_settings)

	#
	# build positive .vec files
	#
	opencv_haar_cascade_cmds.create_vector_file(sample_settings)

	#
	# train
	#
	number_of_stages = 5
	opencv_haar_cascade_cmds.train_cascades(sample_settings,number_of_stages)

	#
	# test detection
	#
	#cascade_file_path = '../haar_cascades/data/working_data/cascades/positive_basketballs/cascade.xml'
	#test_detection.test_cascade_recognition(cascade_file_path,1.01,1)
