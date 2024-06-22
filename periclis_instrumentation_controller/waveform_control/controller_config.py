# DAT/EMI - Electronics and Microelectronics Department
# Redistribution, modification or use of this software in source or binary
# forms is permitted as long as the files maintain this copyright. 

###############################################################################
# DAT/EMI and the Brazilian Center for Research in Energy and Materials (CNPEM)
# are not liable for any misuse of this material.
#
# @file controller_config.py
#
# @brief CLI for controlling Oscilloscope, Wavegenerator and TestVector.
#
# @author Pedro Trindade 
# @author Eric Sonagli Abbade.
# @date 24/04/2024
###############################################################################
from pathlib import Path 

CONTROLLER_NAME = 'WaveformController'
RESOURCE_DIR = Path('./data/configuration_files/')
FILE_NAME='waveform_config'
DEFAULT_CONFIGURATIONS = 'default_waveform_config'
INPUT_FORMAT = '.csv'
