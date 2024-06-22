# DAT/EMI - Electronics and Microelectronics Department
# Redistribution, modification or use of this software in source or binary
# forms is permitted as long as the files maintain this copyright. 

###############################################################################
# DAT/EMI and the Brazilian Center for Research in Energy and Materials (CNPEM)
# are not liable for any misuse of this material.
#
# @file resource_manager.py
#
# @brief CLI for controlling OScilloscope, Wavegenerator and TestVector.
#
# @author Pedro Trindade 
# @author Eric Sonagli Abbade.
# @date 24/04/2024
###############################################################################

import logging 
import pyvisa as visa

BYPASS_LABEL = 'BYPASS'

class PeriCLIsResourceManager(visa.ResourceManager):
    def __init__(self) -> None:
        super().__init__()
    
    def connect_controller(self, controllerClass, resourceLabel=BYPASS_LABEL):
        try:
            # This bypass if you want to connect without 
            # using a resource 
            if resourceLabel == BYPASS_LABEL:
                self.current_controller = controllerClass()
            else:
                self.current_controller = controllerClass(resourceLabel)

        except Exception as error:
            logging.exception(f"Not Able To Connect: {error}")
            raise

        return True    

    def list_services(self) -> dict:
        try:
            return self.current_controller.list_services()
        except:
            logging.exception("No Current Controller")

    def disconnect_resource(self):
        self.current_controller.disconnect()
