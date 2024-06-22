# DAT/EMI - Electronics and Microelectronics Department
# Redistribution, modification or use of this software in source or binary
# forms is permitted as long as the files maintain this copyright. 

###############################################################################
# DAT/EMI and the Brazilian Center for Research in Energy and Materials (CNPEM)
# are not liable for any misuse of this material.
#
# @file cli_service_manager.py
#
# @brief CLI for controlling OScilloscope, Wavegenerator and TestVector.
#
# @author Pedro Trindade 
# @author Eric Sonagli Abbade.
# @date 24/04/2024
###############################################################################

from periclis_instrumentation_controller.resource_manager.resource_manager import PeriCLIsResourceManager
from periclis_instrumentation_controller.utils.decorators import service2print

from cmd import Cmd as cmd 

class CMDServiceManager(cmd):
    
    def insert_controller_services(self, resource_manager : PeriCLIsResourceManager):        
        self.current_services = resource_manager.list_services()
        for service in self.current_services:
            func = getattr(resource_manager.current_controller, service)
            setattr(cmd, 'do_' + str(service), func) 
                
    def delete_services_method(self): #Deactivates the services and their TAB completion after the controller is disconnected.
        for method in self.current_services:
            delattr(cmd, 'do_' + str(method))
    
    def cmd_func_mangling(self, resource_manager : PeriCLIsResourceManager, method_name): 
        attr_to_change = getattr(resource_manager.current_controller, method_name)
        return service2print(attr_to_change)

    def add_services(self, service_list : list[str]):
        for method_name in service_list:
            setattr(self, 'do_' + method_name,  
                    self.cmd_func_mangling(method_name))
            

