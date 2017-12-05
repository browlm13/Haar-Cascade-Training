#!/usr/bin/env python

# internal
import logging
import os

# my lib
from src import data_paths

# external
import cv2
import numpy as np

# logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

"""
	Image Editing Module
"""

#
# Reading And Writing Images
#

def load_images(dir_path):
	""" Read cv2 images from directory path parameter and return array. """

	#dir_path = data_paths.directory_path(__file__,'/data/raw_image_sets')
	#dir_path = data_paths.directory_path(__file__, dir_path)

	# ensure directory exists
	assert os.path.exists(dir_path)
	assert os.path.isdir(dir_path)

	#load images files into array
	files = [f for f in os.listdir(dir_path)]
	images = []
	for f in files:
		file_path = os.path.join(dir_path, f)
		try:	images.append(cv2.imread(file_path))
		except: logger.info('unable to load %s', file_path)

	# ensure images were loaded into array
	assert len(images) > 0

	logger.info('loaded %d images', len(images))
	return images

def write_images(images, file_paths):
	""" write cv2 images to file paths at coresponding indexs """

	assert len(images) == len(file_paths)
	logger.info('Writing %d images', len(images))

	for img, fpath in zip(images, file_paths):
		directory_path = os.path.dirname(fpath)
		if not os.path.exists(directory_path):
			os.makedirs(directory_path)
		cv2.imwrite(fpath, img)

	logger.info('Finished writing %d images', len(images))

#
# Images Transformations
#

def rotate_image(image, angle):
	""" Accept cv2 image and rotates it about its center 
		counter clockwise according to angle parameter in degrees. """

	# locate image center
	image_center = tuple(np.array(image.shape)/2)

	# define transformation matrix
	transformation_matrix = cv2.getRotationMatrix2D(image_center, angle, 1.0)

	# apply transformation
	rotated_image = cv2.warpAffine(image, transformation_matrix, image.shape, flags=cv2.INTER_LINEAR)
	
	return rotated_image

def resize_images(image_array, dimesions):
	""" Accepts an array of cv2 images and a tuple desired dimesions (width, height) 
		and returns an array of resized images. """

	resized_images = []
	for img in image_array:
		resized_images.append(cv2.resize(img,dimesions))

	logger.info('%d images resized', len(resized_images))
	return resized_images


def breakup_image(image, sub_image_dimesions):
	""" Accepts a cv2 image and a tupple specifying desired size of 
	sub_images (sub_images_width, sub_images_height), then returns array of generated sub_images. """

	# original image dimesions
	width, height = image.shape[:2]

	#sub image dimesions
	sub_images_width, sub_images_height = sub_image_dimesions

	sub_images = []

	# begin first sub_image at origin (0,0), top left corner of original image
	# croping formula: y:h, x:w
	# sub image boundry markers
	x_left_marker, x_right_marker, 	= 0, sub_images_width
	y_bottom_marker, y_top_marker 	= 0, sub_images_height

	while y_bottom_marker <= height:
		while x_left_marker <= width:

			# crop image
			crop = image[y_bottom_marker:y_top_marker, x_left_marker:x_right_marker]

			# shift x position markers
			x_left_marker 	= 	x_right_marker
			x_right_marker	+= 	sub_images_width

			# add crop to sub_image list iif it meets specified dimensions
			new_width, new_height = crop.shape[:2]
			if (new_width == sub_images_width) and (new_height == sub_images_height):
				sub_images.append(crop)

		# shift x position markers
		y_bottom_marker += sub_images_height
		y_top_marker 	+= sub_images_height

		# reset x position markers
		x_left_marker, x_right_marker = 0, sub_images_width

	logger.info('%d sub images generated', len(sub_images))
	return sub_images

#
# Images Color Adustments
#

def grayscale(image_array):
	""" Converts array of images to grayscale and return new array. """

	grayscale_images = []
	for img in image_array:
		try:
			grayscale_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			grayscale_images.append(grayscale_img)
		except: logger.info('unable to convert image to grayscale')

	logger.info('%d images converted to grayscale', len(grayscale_images))
	return grayscale_images

def adjust_gamma(image, gamma=1.0):
	""" Adjust cv2 image gamma and return new image.
		source: https://stackoverflow.com/questions/33322488/how-to-change-image-illumination-in-opencv-python/41061351"""
	
	# build a lookup table mapping the pixel values [0, 255] to
	# their adjusted gamma values
	invGamma = 1.0 / gamma
	table = np.array([((i / 255.0) ** invGamma) * 255
		for i in np.arange(0, 256)]).astype("uint8")
 
	# apply gamma correction using the lookup table
	return cv2.LUT(image, table)

#
# Sample Generation Tools For Expanding Sample Image Array
#

def expand_image_array_vary_brightness(image_array, gamma_range, number):
	""" Expand array of cv2 images by varying brightness levels 
		specified by the parameters detaling gamma_range (tuple(low,high)) 
		and number of images to generate. Suggestion: keep gamma range between 0.5 and 2."""

	# assert number is valid
	assert number > 0

	# ensure gamma range is valid
	low, high = gamma_range
	assert low > 0
	assert low < high

	# calculate step size
	step_size = (high - low) / float(number)
	
	# calculate gamma values
	gamma_values = np.arange(low, high, step_size)

	# generate new images
	expanded_image_array = []
	for img in image_array:
		for g in gamma_values:
			gamma_adjusted_img = adjust_gamma(img,g)
			expanded_image_array.append(gamma_adjusted_img)

	logger.info('%d images in new set after varying brightness', len(expanded_image_array))
	return expanded_image_array

def add_rotated_images(image_array):
	""" Expand array of cv2 images by rotating images in 90 increments. """

	expanded_image_array = []
	for img in image_array:
		expanded_image_array.append(img)
		expanded_image_array.append(rotate_image(img, 90))
		expanded_image_array.append(rotate_image(img, 180))
		expanded_image_array.append(rotate_image(img, 270))

	logger.info('%d images in new set after varying brightness', len(expanded_image_array))
	return expanded_image_array

def expand_image_array_by_breaking_images(image_array, sub_image_dimesions, sub_images_per_image):
	""" Expand array of cv2 images by breaking up images into parts.
		Parameter is image list and tuple containing dimesions of sub images. """

	expanded_image_array = []
	if sub_images_per_image > 1:	# [Todo]: imgrpove segmenting
		for img in image_array:						
				expanded_image_array += breakup_image(img, sub_image_dimesions)[:sub_images_per_image]
		return expanded_image_array
	else:
		return image_array

"""
def expand_image_array_by_breaking_images(image_array, sub_image_dimesions):
	#Expand array of cv2 images by breaking up images into parts.
	#	Parameter is image list and tuple containing dimesions of sub images.

	expanded_image_array = []
	for img in image_array:
		expanded_image_array += breakup_image(img, sub_image_dimesions)
	return expanded_image_array

def sub_imagesize(img, sub_images_width=100, sub_images_height=100):
	images = []
	# Croping Formula ==> y:h, x:w
	idx, x_left_marker, x_right_marker,  = 1, 0, sub_images_width
	y_bottom_marker, y_top_marker = 0, sub_images_height
	#img = cv2.imread(image_path)
	#height, width, dept = img.shape
	width, height = img.shape[:2]
	while y_bottom_marker <= height:
		while x_left_marker <= width:
			crop = img[y_bottom_marker:y_top_marker, x_left_marker:x_right_marker]
			x_left_marker=x_right_marker
			x_right_marker+=sub_images_width
			cropped_image_path = "crop/crop%d.png" % idx
			#cv2.imwrite(cropped_image_path, crop)
			#check size
			new_width, new_height = crop.shape[:2]
			if (new_width == sub_images_width) and (new_height == sub_images_height):
				images.append(crop)
			idx+=1
		y_bottom_marker += sub_images_height
		y_top_marker += sub_images_height
		x_left_marker, x_right_marker = 0, sub_images_width
	return images

def sub_images_images(image_array, sub_images_dim_tuple):
	sub_images_width, sub_images_height = sub_images_dim_tuple
	full_image_array = []
	for img in image_array:
		full_image_array += sub_imagesize(img,sub_images_width, sub_images_height)
	return full_image_array
"""