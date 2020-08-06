# coding: utf-8

import yaml
import os.path as path
import warnings

warnings.filterwarnings("ignore")

# Open the configuration file
# ---------------------------

with open(path.join(path.dirname(__file__), "CONFIG.yml"), 'r') as f:
	config_parameters = yaml.load(f, Loader=yaml.FullLoader)
    
# Define the main path (can be useful later to always have access to the path
# where to save the data)
# -----------------------

main_path = path.abspath(config_parameters['Path'])

