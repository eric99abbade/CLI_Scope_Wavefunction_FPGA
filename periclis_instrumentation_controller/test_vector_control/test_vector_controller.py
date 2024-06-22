# DAT/EMI - Electronics and Microelectronics Department
# Redistribution, modification or use of this software in source or binary
# forms is permitted as long as the files maintain this copyright. 

###############################################################################
# DAT/EMI and the Brazilian Center for Research in Energy and Materials (CNPEM)
# are not liable for any misuse of this material.
#
# @file test_vector_controller.py
#
# @brief CLI for controlling OScilloscope, Wavegenerator and TestVector.
#
# @author Pedro Trindade 
# @author Eric Sonagli Abbade.
# @date 24/04/2024
###############################################################################

from periclis_instrumentation_controller.utils.decorators import get_services
from periclis_instrumentation_controller.test_vector_control.test_vector_resource_handler import TestVectorResourceHandler

class testvector_controller(TestVectorResourceHandler):
    # Get resource from visa resource manager
    def __init__(self, resource=None): 
        super().__init__(resource)
        
    def list_services(self) -> dict:
            return get_services(controler_name='TestVectorController')

    def disconnect(self):
        pass #There is no need to do anything since testvector does not start any communication processes.
   
        