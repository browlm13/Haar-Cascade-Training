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
from src import opencv_haar_cascade_cmds_v2 as opencv_haar_cascade_cmds
from src import test_detection

# logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def change_to_root_directory():
	full_path = os.getcwd()
	segments = full_path.split('/')
	for s in reversed(segments):
		if s == 'haar_cascades':
			break
		else:
			os.chdir('..')

def generate_samples():

	#working directory needs to be root, assume this file exits in root directory
	change_to_root_directory()

	# config file
	sample_settings = config_handler.sample_settings(data_paths.get_config_file_path())

	# generate samples and info files for all raw image sets
	create_samples.generate_samples_for_all_raw_image_sets(sample_settings)

def build_positive_vectors():

	#working directory needs to be root, assume this file exits in root directory
	change_to_root_directory()

	# config file
	sample_settings = config_handler.sample_settings(data_paths.get_config_file_path())

	# build positive .vec files
	opencv_haar_cascade_cmds.create_vector_file(sample_settings)

def train_model(model_name, positive_dataset_name, negitive_dataset_name, numPos, number_of_stages):
	
	#working directory needs to be root, assume this file exits in root directory
	change_to_root_directory()

	# config file
	sample_settings = config_handler.sample_settings('config.ini') 	#must remove ../ when accessing in root

	# train 
	opencv_haar_cascade_cmds.train_cascades(model_name, positive_dataset_name, negitive_dataset_name, sample_settings, numPos, number_of_stages)

def test_cascade_recognition(cascade_file_path, scaleFactor, minNeighbors): 

	#working directory needs to be root, assume this file exits in root directory
	change_to_root_directory()

	#test detection
	test_detection.test_cascade_recognition(cascade_file_path,scaleFactor,minNeighbors)

if __name__ == '__main__':

	# generate samples and info files for all raw image sets
	generate_samples()

	# build positive .vec files
	build_positive_vectors()

	# train
	model_name = 'mock1'
	positive_dataset_name = 'positive_basketballs'
	negitive_dataset_name = 'negitive_backgrounds'
	number_of_stages = 1
	numPos = 10
	train_model(model_name, positive_dataset_name, negitive_dataset_name, numPos, number_of_stages)

	# test detection
	cascade_file_path = 'data/working_data/cascades/mock1/cascade/cascade.xml'
	test_cascade_recognition(cascade_file_path, 1.03, 2)

