# DAT/EMI - Electronics and Microelectronics Department
# Redistribution, modification or use of this software in source or binary
# forms is permitted as long as the files maintain this copyright. 

###############################################################################
# DAT/EMI and the Brazilian Center for Research in Energy and Materials (CNPEM)
# are not liable for any misuse of this material.
#
# @file cmd_base.py
#
# @brief CLI for controlling OScilloscope, Wavegenerator and TestVector.
#
# @author Pedro Trindade 
# @author Eric Sonagli Abbade.
# @date 24/04/2024
###############################################################################

import time
import cmd 
import os

from periclis_instrumentation_controller.utils.color_handling import *
from periclis_instrumentation_controller.utils.file_parsing import *
from periclis_instrumentation_controller.resource_manager.resource_manager import PeriCLIsResourceManager
from periclis_instrumentation_controller.utils.args_handling import cmd_parse_input

from periclis_instrumentation_controller.cli.cli_autocompletion import CMDAutocompletion
from periclis_instrumentation_controller.cli.cli_service_manager import CMDServiceManager
from periclis_instrumentation_controller.cli.cmd_resource_connector import CMDResourceConnector, NOT_CONNECTED, NO_CONTROLLER, ALIAS_FOLDER, ALIAS_FILENAME, ALIAS_PATH 
from periclis_instrumentation_controller.cli.cmd_config import set_cmd_config, set_cmd_config_to_default, CMD_LIST, AVAILABLE_CONTROLLERS
from periclis_instrumentation_controller.cli.str_formatting import *
from periclis_instrumentation_controller.cli.emi_banner import EMI_BANNER

class CMDBase(cmd.Cmd): 

    connected_resource_name = NOT_CONNECTED 
    current_controller = NO_CONTROLLER

    available_services = {} 

    autocompleter : CMDAutocompletion = None
    resource_manager : PeriCLIsResourceManager = None
    service_manager : CMDServiceManager = None
    resource_connector : CMDResourceConnector = None

    
    intro = get_blue("\n" + EMI_BANNER + "\n") + \
            get_blue("\n >>>> Welcome to the Programmable-Environment for Reliable Instrumentation CLI System (PeriCLIs)! <<<< \n") + \
            get_green("\n > Command Options: " + \
                        get_format_cmd_str(CMD_LIST) + "\n")

    def __init__(self):
        super().__init__()
        self.resource_manager = PeriCLIsResourceManager()

        # Define the prompt for the command line
        self.prompt = f'(PeriCLIs - {self.connected_resource_name}' +  \
                      f'- {self.current_controller})> ' 
 
        self.available_controllers = AVAILABLE_CONTROLLERS

        self.connection_succeded = False #Connection with controller.
        #Completes Controllers automatically with TAB:
        self.autocompleter = CMDAutocompletion()
        self.autocomplete_commands = [command['descr'] for command in CMD_LIST]    
        self.autocompleter.add_cmd_autocompletion(self, self.autocomplete_commands)  
        
        self.service_manager = CMDServiceManager()
        self.resource_connector = CMDResourceConnector()
        self.available_resources = self.resource_connector.update_available_resources(self.resource_manager)    
   
    # Handles user input into a customized manner:   
    def onecmd(self, line):
        self.case_sensitive = line.split() #Original string, with case sensitivity.
        line=line.lower() #Makes the CLI case insentive.
        return cmd_parse_input(self, line) 

    def do_list_commands(self, arg = None):
            print( get_green("\n > Command Options: " + \
                            get_format_cmd_str(CMD_LIST) + "\n" ))

    def do_test_demonstration(self, arg=None):
            if arg:
                print(arg)
            """Say hello"""
            print("Hello!")
            
    def do_services_list(self, arg = None):
        if  self.current_controller == NO_CONTROLLER:
            print_red("\nPlease connected to a resource/controller\n")
        else:
            print(get_green("\n> Available Services: \n" + \
                  get_format_str_from_dict(self.available_services)) + "\n")
            
            
    def get_available_services(self):
        return self.resource_manager.list_services()
    
    def do_present_controllers(self, arg=None):
        print("\nControllerID \t ControllerName")
        print(*['\t' + str(idx) + '\t' + controller + '\n' 
                for idx, controller in enumerate(self.available_controllers.keys())])

    def do_find_resources(self, arg = None):
        self.available_resources = self.resource_connector.update_available_resources(self.resource_manager)
        print_blue("\n >Available Resources:")  
        print_green("\nResourceID \t ResourceLabel")
        print(*['\t' + str(idx) + '\t' + resource + '\n' 
                for idx, resource in enumerate(self.resource_connector.available_resources)])
  
    def do_connect_resource(self, args):
        self.alias_use = False #Variable that inidicates use of alias.
        (args, self.alias_use, self.alias_name) = self.resource_connector.check_controller_aliases(args, read_file(ALIAS_PATH, '.json'), self.alias_use)
        if self.connected_resource_name != NOT_CONNECTED:
            self.do_disconnect()
            print_red("Disconnected from the current controller!")

        self.connection_succeded = False

        try:
            controller = self.available_controllers[args[1]] 

            if self.alias_use: #With alias the resource is already in the argument.
                resourceLabel = args[0]
                self.connection_succeded = self.resource_manager.connect_controller(controller, resourceLabel)
            else:
                if int(args[0]) == -1: # if we receive a value of -1 to the resource we connect without.
                    self.connection_succeded = self.resource_manager.connect_controller(controller)
                else: #Without alias, it will be needed to find the resource.               
                    resourceLabel = self.resource_connector.available_resources[int(args[0])]            
                    self.connection_succeded = self.resource_manager.connect_controller(controller, resourceLabel)
    
        except Exception as error:
            print(f"Something went wrong in the Controller/Resource Parsing: {error}")

        if self.connection_succeded:
            self.service_manager.insert_controller_services(self.resource_manager) 
            

            set_cmd_config(self, args[0], controller, 
                           connected_to_resource=True, alias_use = self.alias_use, alias_name = self.alias_name)

            print_blue("\nConnection Succeded!") 
            self.do_services_list()

        else:
            print_red("\tCould not connect to Device ;-;")
            
    def do_disconnect(self, args=None):
        if self.connected_resource_name == NOT_CONNECTED:
            print_red("\nNot Connected to a Resource\n")
        else:
            self.resource_manager.disconnect_resource()
            self.service_manager.delete_services_method()

        set_cmd_config_to_default(self)

    
    def do_eof(self, args=None): #Allows the use of sequences on .txt files (scripts folder).
        return True

    def do_alias(self, args=None):
        alias, controller_name, resource_id= check_aliases(self.case_sensitive, AVAILABLE_CONTROLLERS) #Will be used case sensitive arguments.      
        restrictions = ["resource_id", "alias"]
        alias_data = {
            "alias": alias.lower(),
            "controller_name": controller_name.lower(),
            "resource_id": resource_id #Resource will be case sensitive, because it might be the case that resource needs upper case.           
        }                
        if not os.path.exists(ALIAS_FOLDER): # Check if 'alias' folder exists, if not create it.
            os.makedirs(ALIAS_FOLDER)
        add_config(alias_data, ALIAS_PATH , '.json', restrictions)
        print(f"Alias {get_blue(alias)} associated with Controller {get_green(controller_name)} and Resource ID {get_green(resource_id)} has been saved.")
   
    def do_alias_delete(self, args=None):
        alias = first_list_argument(args)
        erase_config(alias, ALIAS_PATH , '.json', 'alias')

    def do_alias_list(self, args=None):
        data_read =  read_file(ALIAS_PATH, '.json')
        for item in data_read:
            print(f"Alias: {get_blue(item["alias"])} associated with Controller:{get_green(item["controller_name"])} and ID:{get_green(item["resource_id"])}")
    
    def do_delay(self, arg=None): #Finish program execution.        
        print_blue(f"Wait {arg} seconds...")
        time.sleep(float(arg))
        print_blue(f"Wait time finished!")
        #return True  # Returning True exits the command loop   
    
    def do_quit(self, arg=None): #Finish program execution.        
        print_red("\nQuitting...\n")
        return True  # Returning True exits the command loop   
    
#periclis < ./scripts/test.txt