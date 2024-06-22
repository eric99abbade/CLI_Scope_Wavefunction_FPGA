# DAT/EMI - Electronics and Microelectronics Department
# Redistribution, modification or use of this software in source or binary
# forms is permitted as long as the files maintain this copyright. 

###############################################################################
# DAT/EMI and the Brazilian Center for Research in Energy and Materials (CNPEM)
# are not liable for any misuse of this material.
#
# @file args_handling.py
#
# @brief CLI for controlling OScilloscope, Wavegenerator and TestVector.
#
# @author Pedro Trindade 
# @author Eric Sonagli Abbade.
# @date 24/04/2024
###############################################################################

from periclis_instrumentation_controller.utils.color_handling import *

import re
from typing import TYPE_CHECKING
# Avoiding type hinting cyclic import
if TYPE_CHECKING:
    from periclis_instrumentation_controller.cli.cmd_base import CMDBase
    
def format_input(arg):
    # Get Arguments Separated (As cmd input is a long string)
    args = arg.split(' ')

    # the first element is the command
    args = args[1:]

    if args:
        #Remove all Empty Strings
        args = [identify_type(i) for i in args if i]

        if len(args) == 1:
            args = args[0]

        return args

# Identify string as just string, integer or float
def identify_type(input: str):
    if input.lower() == 'true' or input.lower() == 'false':
        return bool_defining(input)
    try:
        new_type = float(input) 
        if new_type.is_integer() and not (str(input)).endswith(".0"):
            new_type = int(input)
        input =  new_type
    except ValueError:
        if input[0] == input[-1] == '"':
            input = input[1:-1]
    return input  

def bool_defining(variable):
    if variable.lower() == 'true':
        return True
    elif variable.lower() == 'false':
        return False
    else:
        raise Exception("This variable cannot assume this value! This variable must be compatible with the Python: '"+(str(type(new_type))[8:-2])+"' type!")

def cmd_parse_input(cmdline : "CMDBase", line):
    cmd, arg, line = cmdline.parseline(line)
    arg = format_input(line)
    
    if not line:
        return cmdline.emptyline()
    if cmd is None:
        return cmdline.default(line)
    cmdline.lastcmd = line
    if cmd == '':
        return cmdline.default(line)
    else:
        try:
            func = getattr(cmdline, 'do_' + cmd)
        except AttributeError:
            return cmdline.default(line)
        if arg!=None:
            try:
                return func(arg)
            except TypeError: #Case that the number of arguments is wrong. 
                print_red("Command could not be excuted! Check the correct number of command arguments!")
            except Exception as error: #Case that an exception has been raised by a service.
                print_red("Command could not be excuted!")
                print_red(str(error))
        else: 
            try:
                return func()
            except TypeError: #Case that the number of arguments is wrong.
                print_red("Command could not be excuted! Check the correct number of command arguments!")
            

# Check if ID label is a valid pyvisa name to be used
def check_if_visa_name(resource_label: str):
        is_valid_visa_name = re.search('::INSTR', resource_label)
        if is_valid_visa_name is not None:
            return True
        else: 
            return False
        

        

    

    