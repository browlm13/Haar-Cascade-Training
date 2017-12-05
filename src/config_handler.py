#!/usr/bin/env python

# internal
import configparser

def write_config_file(config_file_path):
	config = configparser.ConfigParser()

	config['POSITIVE_SAMPLES'] = {
											'Sample Image Width' : 20,
											'Sample Image Height' : 20,
											'Rotate Originals': 'True',
											'Number To Generate By Varying Gamma Levels': 4,
											'Gamma Minimum': 0.75,
											'Gamma Maximum': 1.75,
								}
	config['NEGITIVE_SAMPLES'] = {
											'Sample Image Width' : 50,
											'Sample Image Height' : 50,
											'Rotate Originals': 'True',
											'Number To Generate By Varying Gamma Levels': 4,
											'Gamma Minimum': 0.75,
											'Gamma Maximum': 1.75,
											'Number Of Sub Images Per Image': 4
								}
					
	with open(config_file_path, 'w') as configfile:
		config.write(configfile)

def read_config_file(config_file_path):
	config = configparser.ConfigParser()
	config.read(config_file_path)
	sections = config.sections()

def sample_settings(config_file_path):
	""" return dictonary of positive and negitive sample setting dictonaries """

	config = configparser.ConfigParser()
	config.read(config_file_path)
	sections = config.sections()

	settings = {}

	#
	# Positive Sample Settings
	#

	positive_sample_settings = {}

	assert 'POSITIVE_SAMPLES' in config

	positive_sample_settings['Sample Image Width'] = int(config['POSITIVE_SAMPLES']['Sample Image Width'])
	positive_sample_settings['Sample Image Height'] = int(config['POSITIVE_SAMPLES']['Sample Image Width'])
	positive_sample_settings['Rotate Originals'] = config['POSITIVE_SAMPLES']['Rotate Originals']
	positive_sample_settings['Number To Generate By Varying Gamma Levels'] = int(config['POSITIVE_SAMPLES']['Number To Generate By Varying Gamma Levels'])
	positive_sample_settings['Gamma Minimum'] = float(config['POSITIVE_SAMPLES']['Gamma Minimum'])
	positive_sample_settings['Gamma Maximum'] = float(config['POSITIVE_SAMPLES']['Gamma Maximum'])

	# Allow only value of 1
	positive_sample_settings['Number Of Sub Images Per Image'] = 1


	settings['POSITIVE_SAMPLES'] = positive_sample_settings

	#
	# Positive Sample Settings
	#

	negitive_sample_settings = {}

	assert 'NEGITIVE_SAMPLES' in config

	negitive_sample_settings['Sample Image Width'] = int(config['NEGITIVE_SAMPLES']['Sample Image Width'])
	negitive_sample_settings['Sample Image Height'] = int(config['NEGITIVE_SAMPLES']['Sample Image Width'])
	negitive_sample_settings['Rotate Originals'] = config['NEGITIVE_SAMPLES']['Rotate Originals']
	negitive_sample_settings['Number To Generate By Varying Gamma Levels'] = int(config['NEGITIVE_SAMPLES']['Number To Generate By Varying Gamma Levels'])
	negitive_sample_settings['Gamma Minimum'] = float(config['NEGITIVE_SAMPLES']['Gamma Minimum'])
	negitive_sample_settings['Gamma Maximum'] = float(config['NEGITIVE_SAMPLES']['Gamma Maximum'])
	negitive_sample_settings['Number Of Sub Images Per Image'] = int(config['NEGITIVE_SAMPLES']['Number Of Sub Images Per Image'])

	settings['NEGITIVE_SAMPLES'] = negitive_sample_settings

	#
	# Return
	#
	return settings



