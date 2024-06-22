# DAT/EMI - Electronics and Microelectronics Department
# Redistribution, modification or use of this software in source or binary
# forms is permitted as long as the files maintain this copyright. 

###############################################################################
# DAT/EMI and the Brazilian Center for Research in Energy and Materials (CNPEM)
# are not liable for any misuse of this material.
#
# @file file_parsing.py
#
# @brief CLI for controlling OScilloscope, Wavegenerator and TestVector.
#
# @author Pedro Trindade 
# @author Eric Sonagli Abbade.
# @date 24/04/2024
###############################################################################
from periclis_instrumentation_controller.scope_control.device_specific_commands import ACCEPTED_TRIGGER_TYPES, ACCEPTED_CHANNELS, ACCEPTED_TRIGGER_COUPLING, ACCEPTED_TRIGGER_SLOPE
from periclis_instrumentation_controller.test_vector_control.specific_commands import ACCEPTED_WAVE_TYPE
from periclis_instrumentation_controller.utils.arguments_error_functions import errors_arguments_mapping
import periclis_instrumentation_controller.utils.errors_handling as errors_handling
from periclis_instrumentation_controller.utils.color_handling import *
import periclis_instrumentation_controller.utils.errors_handling as errors_handling
from periclis_instrumentation_controller.utils.configuration_variables import *


configurations_mapping = {
    'WaveformController': WaveformController_Configurations,
    'ScopeController': ScopeController_Configurations,
    'TestVectorController': TestVectorController_Configurations
}

options_mapping = {
    'ACCEPTED_TRIGGER_TYPES': ACCEPTED_TRIGGER_TYPES,
    'ACCEPTED_CHANNELS': ACCEPTED_CHANNELS,
    'ACCEPTED_TRIGGER_COUPLING': ACCEPTED_TRIGGER_COUPLING,
    'ACCEPTED_TRIGGER_SLOPE': ACCEPTED_TRIGGER_SLOPE,
    'ACCEPTED_WAVE_TYPE': ACCEPTED_WAVE_TYPE
}

def test_value(self, data_to_write: list, controller: str = None): #Guarantees that variable is according to some pre-defined rules.
    (variable, value) = data_to_write
    rounding_places = get_round_places(self)
    func = None
    func, restriction_conditions, restriction = try_get_restrictions(controller, variable)
    if str(func).startswith("<function first_list_argument"): #In case of boolean variable, it will already be tested if the new variable is boolean.
        return
    if func: #In case, it has been found a restriction function for this variable, it will be executed.
        argument_index = errors_arguments_mapping[restriction]
        standard_function_arguments = replace_argument_value(argument_index, value, "for changing the value", variable, rounding_places)
        function_arguments = check_extra_arguments(standard_function_arguments, restriction, restriction_conditions) #Checks if the function has extra arguments.
        func(*function_arguments)

def get_round_places(self):
    try:
        rounding_places_configurations = self.rounding_places_configurations #If there is a variable with the defined value, it will be used.
        return rounding_places_configurations
    except:
        return 12 #If there is not any variable, it will be used 12 as default.
    
def try_get_restrictions(controller, variable):
    try:
        restriction_conditions = getattr(configurations_mapping[controller], variable)
        restriction = get_function_restriction(restriction_conditions) #Chose the string corresponding to the function.
        func = getattr(errors_handling, restriction) #Funtcion for checking the variable conditions.
        return func, restriction_conditions, restriction
    except:
        print_yellow("Variable restriction not found")
    
def get_function_restriction(restriction_conditions):
    if isinstance(restriction_conditions, tuple):
        return str(restriction_conditions[0])
    else:
        return restriction_conditions

def replace_argument_value(template_tuple: tuple, value, command: str, argument: str, rounding_places: str): #Function for identifying the arguments and replacing them with the correct values.
    template_list = list(template_tuple) #Convert the tuple to a list to perform replacement.        
    template_list[template_list.index("argument_value")] = value #Replace "argument_value" with its value.
    template_list[template_list.index("command")] = command #Replace "argument_value" with its value.
    template_list[template_list.index("argument")] = argument #Replace "argument_value" with its value.
    template_list[template_list.index("rounding_places")] = rounding_places #Replace "rounding_places" with its value.
    return template_list

def check_extra_arguments(template_tuple: tuple, restriction: str, restriction_conditions):
    template_list = list(template_tuple) #Convert the tuple to a list to perform replacement. 
    if restriction == "error_interval" or restriction == "error_excludent_interval":        
        template_list[template_list.index("minimum")] = restriction_conditions[1] #Replace "minimum" with its value.
        template_list[template_list.index("maximum")] = restriction_conditions[2] #Replace "maximum" with its value.
    elif restriction == "check_list_options":
        template_list[template_list.index("accepted_list")] = (dir(options_mapping[restriction_conditions[1]])) #Replace "accepted_list" with its value.
    return template_list