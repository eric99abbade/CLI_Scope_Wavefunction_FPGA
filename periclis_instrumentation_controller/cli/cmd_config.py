# DAT/EMI - Electronics and Microelectronics Department
# Redistribution, modification or use of this software in source or binary
# forms is permitted as long as the files maintain this copyright. 

###############################################################################
# DAT/EMI and the Brazilian Center for Research in Energy and Materials (CNPEM)
# are not liable for any misuse of this material.
#
# @file cmd_config.py
#
# @brief CLI for controlling OScilloscope, Wavegenerator and TestVector.
#
# @author Pedro Trindade 
# @author Eric Sonagli Abbade.
# @date 24/04/2024
################################################################################

from periclis_instrumentation_controller.cli.cmd_resource_connector import NO_CONTROLLER, NOT_CONNECTED

from periclis_instrumentation_controller.waveform_control.waveform_controller import waveform_controller
from periclis_instrumentation_controller.scope_control.scope_controller import scope_controller
from periclis_instrumentation_controller.test_vector_control.test_vector_controller import testvector_controller

from periclis_instrumentation_controller.utils.color_handling import *

# Avoiding type hinting cyclic import
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cmd_base import CMDBase

AVAILABLE_CONTROLLERS = {waveform_controller.__name__: waveform_controller, 
                         scope_controller.__name__: scope_controller,
                         testvector_controller.__name__: testvector_controller}


CMD_LIST = [{'descr': 'alias', 'args': 'alias controller_name resource_id (resource_id can be UPPER CASE)'}, 
            {'descr': 'alias_delete', 'args': 'alias'},
            {'descr': 'alias_list'},    
            {'descr': 'connect_resource', 'args': 'ResourceId ControllerName'},
            {'descr': 'delay', 'args': 'delay_time (seconds)'},
            {'descr': 'disconnect'},
            {'descr': 'find_resources'},
            {'descr': 'list_commands'},
            {'descr': 'present_controllers'}, 
            {'descr': 'quit'},
            {'descr': 'services_list'}
            ]
    
def set_cmd_config_to_default(cmd : "CMDBase"):
    set_cmd_config(cmd)
                        
def set_cmd_config(cmd: "CMDBase", 
                   resource_name: str = NOT_CONNECTED,
                   current_controller: str = NO_CONTROLLER,
                   connected_to_resource : bool = False,
                   alias_use: bool = False,
                   alias_name: str = None):

    cmd.connected_resource_name = resource_name 
    cmd.current_controller =  current_controller
    
    if connected_to_resource:
        # Define the prompt for the command line
        #@TODO fix color not working only in prompt
        if alias_use: #Case that user is using an alias.
            cmd.prompt = get_green('(') + get_blue(f'PeriCLIs - Connected to Device - {alias_name}' + \
                         f' - {current_controller.__name__}') + get_green(')> ')
        else:
            cmd.prompt = get_green('(') + get_blue(f'PeriCLIs - Connected to Device {resource_name}' + \
                         f' - {current_controller.__name__}') + get_green(')> ')

        cmd.available_services = cmd.get_available_services() 

        if cmd.available_services != {}:
            cmd.autocompleter.add_cmd_autocompletion(cmd, list(cmd.available_services.keys())) 
    else:
        # Define the prompt for the command line
        cmd.prompt = f'(PeriCLIS - {NOT_CONNECTED}' +  \
                     f'- {NO_CONTROLLER})> ' 
        cmd.available_services = {}

   