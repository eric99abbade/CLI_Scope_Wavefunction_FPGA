# DAT/EMI - Electronics and Microelectronics Department
# Redistribution, modification or use of this software in source or binary
# forms is permitted as long as the files maintain this copyright. 

###############################################################################
# DAT/EMI and the Brazilian Center for Research in Energy and Materials (CNPEM)
# are not liable for any misuse of this material.
#
# @file str_formatting.py
#
# @brief CLI for controlling OScilloscope, Wavegenerator and TestVector.
#
# @author Pedro Trindade 
# @author Eric Sonagli Abbade.
# @date 24/04/2024
###############################################################################

from functools import reduce
from periclis_instrumentation_controller.utils.color_handling import *

## Some utility function to format the strings to print to the cmd

def get_format_cmd_str(cmd_list : list[dict]) -> str:
    formatted_cmd_list = []
    for cmd in cmd_list:
        # Use args only if it exists
        args_str = ', args: ' + cmd.get('args') if cmd.get('args') != None else ""

        formatted_cmd_list = formatted_cmd_list + [f"\n\t - {cmd['descr']}{args_str}"]
    return reduce(lambda a,b: a+b, formatted_cmd_list)

# If you send the service metadata to this it 
# can get you the string in a formatted way
def get_format_str_from_dict(obj_dict: dict[dict]) -> str: 
    obj_dict_str = []    
    if obj_dict is not None:
        for key in obj_dict.keys():
            service_title = get_green("\n\t- " + str(key))
            service_title_args = get_green(str(service_title) + get_blue(", args:"))
            if obj_dict[key] is not None and "args" in obj_dict[key].keys():
                arg = get_blue(str(list(obj_dict[key]["args"].keys()))[1:-1])
                if list(obj_dict[key]["args"].values()) != [None]: #Access services with a list of accepted options.
                    arg = arg + " " + get_green(str(list(obj_dict[key]["args"].values()))[1:-1])                 
                obj_dict_str.append((f'{service_title_args} {arg}').replace("'", ""))
            else:
                obj_dict_str.append((f'{service_title}').replace("'", ""))

    return reduce(lambda a,b: a+b, obj_dict_str)


def get_format_str_from_list(obj_list: list[str]) -> str:
    list_len = len(obj_list)
    obj_list_str = []

    # This part tries to spread horizontally if given too many elements
    if list_len > 10 :
        
        # If not an even number of itens we put one more in the end
        if list_len % 2 == 0 :
            obj_list_str = [f'\t- {obj_list[i]} \t\t- {obj_list[i+1]}\n' for i in range(0,list_len-1,2)]
        else:
            obj_list_str = [f'\t- {obj_list[i]} \t\t- {obj_list[i+1]}\n' for i in range(0,list_len-2,2)]
            obj_list_str.append('\t- ' + obj_list[list_len-1] + '\n')
            
    else:
        obj_list_str = [f'\t- {obj} \n' for obj in obj_list]

    return reduce(lambda a,b: a+b, obj_list_str)

def function_checker(accepted_list): #Removes the undesired elements that start with the "__".
    accepted_list_corrected=[] 
    for element in accepted_list:
        if element[:2]!="__": 
            accepted_list_corrected.append(element)
    return accepted_list_corrected

