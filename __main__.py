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

# logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#raw_images_directory_path = '/data/raw_image_sets'
#sample_images_directory_path = 'data/working_data/generated_samples' 	#WHY!!!!???

if __name__ == '__main__':

	#
	# config file
	#
	sample_settings = config_handler.sample_settings(data_paths.get_config_file_path())

	#
	# generate samples and info files for all raw image sets
	#
	create_samples.generate_samples_for_all_raw_image_sets(sample_settings)



	"""
	# raw positive dataset
	raw_positive_data_set = '/cropped_basketballs'

	# path to raw positive data set
	#raw_positives_path = raw_images_directory_path + raw_positive_data_set
	raw_positives_path = glob.glob('../haar_cascades/data/raw_image_sets/cropped_basketballs')[0]

	# path to generated positive data set
	positive_generated_samples_path = sample_images_directory_path + raw_positive_data_set

	#raw_positives_path = '/data/raw_image_sets/cropped_basketballs'
	#images = image_editing.load_images(raw_positives_path)

	create_samples.create_samples(raw_positives_path, positive_generated_samples_path)
	"""