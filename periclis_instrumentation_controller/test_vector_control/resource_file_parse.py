# DAT/EMI - Electronics and Microelectronics Department
# Redistribution, modification or use of this software in source or binary
# forms is permitted as long as the files maintain this copyright. 

###############################################################################
# DAT/EMI and the Brazilian Center for Research in Energy and Materials (CNPEM)
# are not liable for any misuse of this material.
#
# @file resource_file_parse.py
#
# @brief CLI for controlling OScilloscope, Wavegenerator and TestVector.
#
# @author Pedro Trindade 
# @author Eric Sonagli Abbade.
# @date 24/04/2024
###############################################################################

from periclis_instrumentation_controller.test_vector_control.controller_config import DEFAULT_RESOURCE_DIR, DEFAULT_INPUT_FORMAT
from periclis_instrumentation_controller.utils.file_parsing import read_file

from pathlib import Path
import logging

def resource_file_parse(resource_name: str, 
                        resource_dir: Path = DEFAULT_RESOURCE_DIR,
                        resource_file_format: str = DEFAULT_INPUT_FORMAT):
    """
    Parses a resource file based on the specified format and returns
    the content in the specified file format if it is supported.

    @param resource_name The `resource_name` parameter is a string that represents the
    name of the resource file that you want to parse.

    @param resource_dir  is used to specify the directory where the resource file is 
    located, it defaults to the ambient variable DEFAULT_RESOURCE_DIR in the config script. 

    @param resource_file_format  is used to specify the format of the resource file that is being parsed.
    """

    if not resource_name.endswith(resource_file_format):
        logging.exception("File format not compatible")
    
    resource_path = resource_dir / resource_name 

    #checks if file exists 
    if not resource_path.is_file():
        logging.exception("Resource file does not exist")
        
    
    if resource_name.endswith(".json"):
        return read_file(resource_path, '.json')

    logging.exception("File format not Supported")

    