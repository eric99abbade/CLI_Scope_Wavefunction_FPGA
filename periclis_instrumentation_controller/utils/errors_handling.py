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

import string
from periclis_instrumentation_controller.utils.args_handling import identify_type, bool_defining
from periclis_instrumentation_controller.utils.color_handling import *
from periclis_instrumentation_controller.cli.str_formatting import function_checker

def first_list_argument(variable: str, rounding_places:int = 3): #Checks if the variable is a list, and returns the first argument.
    if isinstance(variable, list): 
        variable=variable[0] #Checks only the first argument if the "variable" is a list.
        if isinstance(variable, int):
            variable=float(variable) #Change int to float (to be printed with points in a more "numeric" format).
        print_yellow('Use only 1 argument! Argument with the value of: '+str(variable)+' was used, other(s) ignored!')
    try:
        variable=round((float(variable)), int(rounding_places)) #Rounds the variable if needed.
    except:
        pass
    return variable 

def check_numerical(variable, rounding_places:int = 3): #Checks if the variable is numerical.
    if (isinstance(variable, int) or isinstance(variable, float)): #Returns True if variable is integer or float.
        return True
    else: #Return False if the variable is not numerical.
        return False
    
def initial_string(variable: str, command_name:str="command", argument_name:str="argument", rounding_places:int = 3): #Combines the command name with the argument name in order to generate a standard string to initiate the error warning.
    if isinstance(variable, int):
            variable=float(variable) #Change int to float (to be printed with points in a more "numeric" format).
    return('The Argument ('+str(argument_name)+') Used After The Service ('+str(command_name)+') was: '
           +str(variable)+'. However, The Argument Must Be ')
    
def error_non_numerical(variable: str, command_name:str="command", argument_name:str="argument", rounding_places:int = 3): #Checks if the variable is numerical.
    variable = first_list_argument(variable, rounding_places) #Use only the first value of the list (if it is actually a list) for the analisys.
    if check_numerical(variable)==False:        
        initial_message=initial_string(variable, command_name, argument_name)        
        raise Exception(initial_message+"Numeric!")
   
def error_negative(variable: str, command_name:str="command", argument_name:str="argument", rounding_places:int = 3): #Checks if the variable is non negative.
    error_non_numerical(variable, command_name, argument_name, rounding_places) #First, checks if it is really a number.
    variable = first_list_argument(variable, rounding_places)
    if variable<0:
        initial_message=initial_string(variable, command_name, argument_name)  
        raise Exception(initial_message+"Non Negative!")
    
def error_non_positive(variable: str, command_name:str="command", argument_name:str="argument", rounding_places:int = 3): #Checks if the variable is positive.
    error_non_numerical(variable, command_name, argument_name, rounding_places) #First, checks if it is really a number.
    variable = first_list_argument(variable, rounding_places)
    if variable<=0:
        initial_message=initial_string(variable, command_name, argument_name)  
        raise Exception(initial_message+"Positive!")
    
def error_interval(variable: str, minimal=0, maximal=0, command_name:str="command", argument_name: str="argument", rounding_places:int = 3): #Checks if the variable is inside a interval.
    error_non_numerical(variable, command_name, argument_name, rounding_places) #First, checks if it is really a number.
    variable = first_list_argument(variable, rounding_places) #First, checks if it is really a number.
    if (variable>maximal) or (variable<minimal): #Since > and < were used, the maximal and minimal points are included in the interval.
        initial_message=initial_string(variable, command_name, argument_name)  
        raise Exception(initial_message+"In The Following Interval: ", minimal, " to ", maximal,"!")
    
def error_excludent_interval(variable: str, minimal=0, maximal=0, command_name:str="command", argument_name: str="argument", rounding_places:int = 3): #Checks if the variable is inside a interval.
    error_non_numerical(variable, command_name, argument_name, rounding_places) #First, checks if it is really a number.
    variable = first_list_argument(variable, rounding_places) #First, checks if it is really a number.
    if (variable>=maximal) or (variable<=minimal): #Since >= and <= were used, the maximal and minimal points are excluded from the interval.
        initial_message=initial_string(variable, command_name, argument_name)  
        raise Exception(initial_message+"In The Following Interval: ", minimal, " to ", maximal,"!")

def equalize_type(old_type, new_type):
    try: #Identyfies correctly the type of variables. 
        old_type = identify_type(str(old_type)) 
        new_type = identify_type(str(new_type)) 
    except:
        pass
    try:
        new_type = type(new_type)(first_list_argument(new_type))
        if isinstance(new_type, bool):
            return bool_defining(str(old_type))
        if type(old_type) != type(new_type):
            print_yellow("Attention! You informed a variable with the Python: '"+(str(type(old_type))[8:-2])+"' type! However, it was changed to the correct Python type for this variable: '"+(str(type(new_type))[8:-2])+"'!")
            old_type = type(new_type)(first_list_argument(old_type))
    except:
        raise Exception("This variable cannot assume this value! This variable must be compatible with the Python: '"+(str(type(new_type))[8:-2])+"' type!")
    if check_numerical(new_type):
        error_non_numerical(old_type) 
    return old_type

def error_file(file:str, format:str="json", command_name:str="command", argument_name:str="argument"): #Checks if the file format is correct.
    if file[-(len(format)+1):]!="."+format:    
        raise Exception(f'Argument used: "{file}" is invalid! Service {command_name} accepted arguments are {format} files!')

def check_list_options(option:str, accepted_list:str, command_name:str="command", argument_name:str="argument", rounding_places:int = 3): #Checks if the variable is inside a defined list.
    accepted_list_corrected=function_checker(accepted_list)
    if option not in (accepted_list_corrected):
        raise Exception(f'Argument used: "{option}" is invalid! Service {command_name} accepted arguments are:\n {accepted_list_corrected}')
    
def check_channels(channel, standard_channel):
    if channel==0:
        return int(standard_channel)
    else:
        channel=first_list_argument(channel, 0)
        error_non_numerical(channel, 0)
        return int(channel)
        
def check_aliases(args, AVAILABLE_CONTROLLERS):
    update_data = list(args)
    if len(update_data) != 4:
        raise Exception("Must inform (controller name) + (VISA ID) +(alias name) after command alias!")     
    alias =  check_alias_name((update_data[1]).lower())
    controller_name = check_controller(update_data[2].lower(), AVAILABLE_CONTROLLERS)
    resource_id = update_data[3] #Since IDs can assume many formats, it will be allowed case sensitivity and it will be responsibility of the user to type the correct one.
    return alias, controller_name, resource_id

def check_alias_name(alias):
    alias = str(alias)
    for index, char in enumerate(alias):
        if char in string.ascii_letters:
            return alias #Case string has a letter caracther. 
        if (index+1) == len(alias): #Case string does not have a letter caracther. 
            raise Exception(f'{get_red(alias)} alias  is invalid! It must contain at least one letter as character')

def check_controller(controller, AVAILABLE_CONTROLLERS):
    if controller in AVAILABLE_CONTROLLERS: #Case controller typed is actually a controller.
        return controller 
    else: #Case controller typed is not a real controller.
        raise Exception(f'{get_red(controller)} is not a controller! Valid controllers are: {get_green(', '.join(list(AVAILABLE_CONTROLLERS.keys())))}')

