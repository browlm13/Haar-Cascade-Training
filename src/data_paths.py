#!/usr/bin/env python

# internal
import logging
import os
import glob

# logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# definitions
root_directory_path = '../haar_cascades'
config_file_path = root_directory_path + '/config.ini'
raw_images_directory_path = root_directory_path + '/data/raw_image_sets'
sample_images_directory_path = root_directory_path + '/data/working_data/generated_samples'
info_files_directory_path = root_directory_path + '/data/working_data/info_files'
vector_files_directory_path = root_directory_path + '/data/working_data/vector_files'


def get_data_sets_info():
	""" return list of dictonaries with image set information """

	all_data_sets = []

	# generate images for all directories in raw_images_directory_path
	for dir in glob.glob(raw_images_directory_path + '/*'):
		image_set_info = {}
		dir_name = os.path.basename(dir)
		image_set_info['set type'], image_set_info['name'] = dir_name.split('_')
		image_set_info['path'] = {}
		image_set_info['path']['raw images directroy'] = dir
		image_set_info['path']['sample images directory'] = sample_images_directory_path + '/' + dir_name
		image_set_info['path']['sample image file path template'] = image_set_info['path']['sample images directory'] + '/' + image_set_info['name'] + '_%d.jpg'
		image_set_info['path']['info file'] = info_files_directory_path + '/' + dir_name + '.txt'
		image_set_info['path']['vector file'] = vector_files_directory_path + '/' + dir_name + '.vec'


		all_data_sets.append(image_set_info)

	return all_data_sets

def get_config_file_path():
	return config_file_path

# not using
def directory_path(file_attribute, path_from_root):
	path_to_root = ".."	#make dynamic
	script_dir = os.path.dirname(file_attribute) 
	rel_path = path_to_root + path_from_root 
	return os.path.join(script_dir, rel_path)
