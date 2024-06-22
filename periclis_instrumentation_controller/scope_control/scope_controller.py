# DAT/EMI - Electronics and Microelectronics Department
# Redistribution, modification or use of this software in source or binary
# forms is permitted as long as the files maintain this copyright. 

###############################################################################
# DAT/EMI and the Brazilian Center for Research in Energy and Materials (CNPEM)
# are not liable for any misuse of this material.
#
# @file scope_controller.py
#
# @brief CLI for controlling OScilloscope, Wavegenerator and TestVector.
#
# @author Pedro Trindade 
# @author Eric Sonagli Abbade.
# @date 24/04/2024
###############################################################################

from periclis_instrumentation_controller.scope_control.scope_reader import ScopeReader
from periclis_instrumentation_controller.scope_control.scope_writer import ScopeWriter
from periclis_instrumentation_controller.scope_control.controller_config import *
from periclis_instrumentation_controller.utils.file_parsing import *
from periclis_instrumentation_controller.utils.decorators import get_services
from periclis_instrumentation_controller.utils.args_handling import check_if_visa_name
from periclis_instrumentation_controller.utils.color_handling import *
import pyvisa as visa

import logging 

class scope_controller(ScopeReader, ScopeWriter):
    # Get resource from visa resource manager
    def __init__(self, resource=None): 
        self.rm = visa.ResourceManager()
         # For the cases that the resources are VISA IDs.
        if resource != None and not check_if_visa_name(resource):
            logging.exception("Not Valid Visa ID")
            raise Exception("Not Valid Visa ID")

        self.scope_generator = self.rm.open_resource(resource) 
        convert_list_variables(self, (RESOURCE_DIR), (FILE_NAME + INPUT_FORMAT), '.csv') #Convert variables from the configuration.csv file to Python variables. 
        self.scope_generator.timeout = (float(self.standard_timeout))*1000 #Sets the initial timeout.
        ScopeReader.__init__(self, self.scope_generator)
        ScopeWriter.__init__(self, self.scope_generator)
        print_blue("Variables used for changing the parameter values will be rounded according to the decimal places defined in the data/scope_config.csv file.")

    def list_services(self) -> dict:
        return get_services(controler_name='ScopeController')
    
    def disconnect(self):
        self.scope_generator.close()
        self.rm.close()

   
        