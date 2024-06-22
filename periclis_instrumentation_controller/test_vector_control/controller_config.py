# DAT/EMI - Electronics and Microelectronics Department
# Redistribution, modification or use of this software in source or binary
# forms is permitted as long as the files maintain this copyright. 

###############################################################################
# DAT/EMI and the Brazilian Center for Research in Energy and Materials (CNPEM)
# are not liable for any misuse of this material.
#
# @file controller_config.py
#
# @brief CLI for controlling OScilloscope, Wavegenerator and TestVector.
#
# @author Pedro Trindade 
# @author Eric Sonagli Abbade.
# @date 24/04/2024
###############################################################################
from pathlib import Path 

CONTROLLER_NAME = 'TestVectorController'
TEST_VECTOR_OUTPUT_PATH = Path('./data/test_vector_output/')
TEST_VECTOR_OUTPUT_DEFAULT_NAME = "testvector{id}"
DEFAULT_RESOURCE_DIR = Path('./data/virtual_resources')
EXTRA_RESOURCE_DIR = 'waveform_generators'
STANDARD_INPUT_FILE = 'basic_generator'
DEFAULT_INPUT_FORMAT = '.json'
DEFAULT_OUTPUT_FORMAT = '.json'