#!/usr/bin/env python

# internal
import logging
import os

# my lib
from src import image_editing
from src import data_paths

# external
import cv2

# logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

"""
	Create Samples From Raw Datasets
"""
def generate_samples(raw_images, sample_settings):
	""" takes sample settings dictonary defined by configuration file and 
		generate samples from raw images according to sample_settings dictonary
		and return samples image list. """

	sample_width = sample_settings['Sample Image Width']
	sample_height = sample_settings['Sample Image Height']
	rotate_images = sample_settings['Rotate Originals']
	gamma_duplication_number = sample_settings['Number To Generate By Varying Gamma Levels']
	gamma_minimum = sample_settings['Gamma Minimum']
	gamma_maximum = sample_settings['Gamma Maximum']
	sub_image_number = sample_settings['Number Of Sub Images Per Image']

	# convert to gray scale
	generated_samples = image_editing.grayscale(raw_images)

	# add rotated images
	if rotate_images:
		generated_samples = image_editing.add_rotated_images(generated_samples)

	# vary brightness
	if gamma_duplication_number > 0:
		gamma_range = (gamma_minimum, gamma_maximum)
		duplication_number = gamma_duplication_number
		generated_samples = image_editing.expand_image_array_vary_brightness(generated_samples,gamma_range,duplication_number)

	# expand by breaking apart images
	image_dimensions = (sample_width,sample_height)
	generated_samples = image_editing.expand_image_array_by_breaking_images(generated_samples,image_dimensions,sub_image_number)

	# resize images
	image_dimensions = (sample_width,sample_height)
	generated_samples = image_editing.resize_images(generated_samples, image_dimensions)

	# return generated sample images list
	return generated_samples

def generate_samples_for_all_raw_image_sets(sample_settings):
	""" takes sample settings dictonary defined by configuration file and 
		generates samples for every directory in raw image sets directory. """

	# raw_image_data_sets
	image_data_sets = data_paths.get_data_sets_info()

	for ds in image_data_sets:

		#
		# load
		#

		logger.info('loading %s raw image data set', ds['name'])
		raw_images = image_editing.load_images(ds['path']['raw images directroy'])

		#
		# generate
		#

		# create samples
		set_type = ds['set type']
		assert set_type in ('positive', 'negitive')
		samples = []
		if set_type == 'positive':
			samples = generate_samples(raw_images, sample_settings['POSITIVE_SAMPLES'])
		if set_type == 'negitive':
			samples = generate_samples(raw_images, sample_settings['NEGITIVE_SAMPLES'])

		#
		# save
		#

		#create file paths
		file_paths = []
		for i in range(len(samples)):
			file_paths.append(ds['path']['sample image file path template'] % (i+1))
		
		# write images
		image_editing.write_images(samples, file_paths)

		# write info file
		### info file path may need modified file path for each file path 
		tail = '\n' #Default Negitive Tail
		if set_type == 'positive':
			sample_width = sample_settings['POSITIVE_SAMPLES']['Sample Image Width']
			sample_height = sample_settings['POSITIVE_SAMPLES']['Sample Image Height']
			image_dimensions = (sample_width,sample_height)
			# using assumtions : num objects, x1, y1, x2 ,y2
			tail = " 1 0 0 %d %d\n" % image_dimensions

		info_file_path = ds['path']['info file']

		#relative paths from info file (not working)
		relative_file_paths = [os.path.relpath(fp, info_file_path) for fp in file_paths]

		#absolute paths
		absolute_file_paths = list(map(os.path.abspath,file_paths))


		#NOTE: opencv_createsamples img -info positive_basketballs.txt -vec ../vector_files/positive_basketballs.vec -w 20 -h 20 -num 500
		#		Must be run from same directory as info file

		tails = [tail] * len(absolute_file_paths)
		pairs = zip(absolute_file_paths, tails)
		lines = [ p[0] + p[1] for p in pairs]
		with open(info_file_path, 'w') as f:
			for l in lines: f.write(l)

