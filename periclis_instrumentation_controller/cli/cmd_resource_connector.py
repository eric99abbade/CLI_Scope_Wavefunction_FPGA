# DAT/EMI - Electronics and Microelectronics Department
# Redistribution, modification or use of this software in source or binary
# forms is permitted as long as the files maintain this copyright. 

###############################################################################
# DAT/EMI and the Brazilian Center for Research in Energy and Materials (CNPEM)
# are not liable for any misuse of this material.
#
# @file cmd_resource_connector.py
#
# @brief CLI for controlling OScilloscope, Wavegenerator and TestVector.
#
# @author Pedro Trindade 
# @author Eric Sonagli Abbade.
# @date 24/04/2024
###############################################################################

import warnings
import os
import glob

from periclis_instrumentation_controller.utils.color_handling import *
from periclis_instrumentation_controller.resource_manager.resource_manager import PeriCLIsResourceManager
from periclis_instrumentation_controller.cli.cli_service_manager import CMDServiceManager
from periclis_instrumentation_controller.cli.str_formatting import *

from pathlib import Path

NOT_CONNECTED = 'Not Connected'
NO_CONTROLLER = 'No Controller'

# Relative to the project root
VIRTUAL_RESOURCES_PATH = Path('./data/virtual_resources/')
PROJECT_ROOT_PATH = Path(f"{Path(__file__).parent}/../..")
ALIAS_FOLDER = 'alias'
ALIAS_FILENAME = 'alias.json'
ALIAS_PATH = os.path.join(ALIAS_FOLDER, ALIAS_FILENAME) # Path to the alias JSON file.

class CMDResourceConnector: 
    
    available_resources = []
    
    def __init__(self) -> None:
        # Changes script dir to root of the project
        # Important for finding the virtual resources
        os.chdir(PROJECT_ROOT_PATH)

    def update_available_resources(self, resource_manager : PeriCLIsResourceManager):
        # Temporarilly ignore warnings
        # @TODO fix this
        # updates available resources list
        warnings.filterwarnings('ignore')
        self.available_resources = list(resource_manager.list_resources())

        virtual_resources=self.list_virtual_resources()
        self.available_resources = self.available_resources + virtual_resources

        warnings.filterwarnings('default')

    def get_parent_dirname(self, path : str):
        return Path(os.path.basename(os.path.dirname(path)))

    def list_virtual_resources(self, extension='json'):
        virtual_resources_regex = str(VIRTUAL_RESOURCES_PATH/ '*' / '*.{}'.format(extension))
        result = glob.glob(virtual_resources_regex)
        result = [str(self.get_parent_dirname(path) / 
                  os.path.basename(path)) for path in result]
        return result

    def connect_resource(self, resource_manager : PeriCLIsResourceManager, resourceLabel, controller):

        connection_succeded = False
        self.update_available_resources()
        connection_succeded = resource_manager.connect_controller(controller, resourceLabel)   
            
        return connection_succeded
            
    def disconnect_resource(self, resource_label : str, service_manager : CMDServiceManager):
        disconnection_succeded = True
        if resource_label == NOT_CONNECTED:
            disconnection_succeded = False
        else:
            service_manager.delete_services_method()

        return disconnection_succeded
    
    def check_controller_aliases(self, args, aliases, alias_use):
        for alias in aliases:
            if args == alias["alias"]: #Case an alias was typed.
                alias_use = True #To inidicate use of alias.
                return (((alias["resource_id"]), (alias["controller_name"])), alias_use, alias["alias"]) #The respective resource ID and controller name will replace 'args'.
        return args, alias_use, None #In case args was not typed, args will be returned.
     