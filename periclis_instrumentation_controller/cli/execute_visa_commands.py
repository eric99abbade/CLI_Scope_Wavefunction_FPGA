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

from periclis_instrumentation_controller.utils.color_handling import *
from periclis_instrumentation_controller.waveform_control.device_specific_commands import WRITE_COMMANDS, ACCEPTED_FUNCTION_TYPES

def visa_read(variable:str, command_name:str="command", argument_name:str="argument"):
    try:
        print(command_name)
        print_concluded_message(variable, command_name, argument_name)
    except: #In case command could not be executed.
        print_red("Problem on the VISA communication!")

def visa_write(clas, command_name, channel, variable, argument_name, generator):
    try:
        generator.write(WRITE_COMMANDS.change_function_type.format(channel = channel, function_type=variable)) 
        print_concluded_message(variable, command_name, argument_name)
    except: #In case command could not be executed.
        print_red("Problem on the VISA communication!")

def print_concluded_message(variable: str, command_name:str="command", argument_name:str="argument"):
    if command_name.startswith("change_"): #Print messages to denote that the change of parameters has been concluded.
        print_green("Service successfully executed and "+str(command_name[len("change_"):])+" changed to: "+str(variable))
