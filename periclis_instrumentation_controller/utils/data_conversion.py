# DAT/EMI - Electronics and Microelectronics Department
# Redistribution, modification or use of this software in source or binary
# forms is permitted as long as the files maintain this copyright. 

###############################################################################
# DAT/EMI and the Brazilian Center for Research in Energy and Materials (CNPEM)
# are not liable for any misuse of this material.
#
# @file data_convertion.py
#
# @brief CLI for controlling OScilloscope, Wavegenerator and TestVector.
#
# @author Pedro Trindade 
# @author Eric Sonagli Abbade.
# @date 24/04/2024
###############################################################################

from fxpmath import Fxp
from periclis_instrumentation_controller.utils.color_handling import *

def convert_fixed(floats : list[float], size, 
                  fraction_size, signed=True) -> Fxp:

    return Fxp(floats, n_word=size,
               n_frac=fraction_size,signed=signed)

def round_variables(variables_to_be_rounded, rounding_cases):    
    rounded_args=[] #List to armazenate the rounded values.
    for i in range(len(variables_to_be_rounded)):  
        if isinstance(variables_to_be_rounded[i], float): #For rounding Floats.      
            rounded_args.append(round(variables_to_be_rounded[i], rounding_cases))                
        else: #For NOT rounding Strings or Ints.
            rounded_args.append(variables_to_be_rounded[i])
    return rounded_args

def remove_channel_prefix(string):
    if string[:2] == "CH":
        return string[2:]
    else:
        return string
    
def convert_binary_on_off(binary):
    if len(binary) == 2:
        binary=binary[:-1]         
    if binary=="1":
        print_green("On")
    else:
        print_green("Off")

def calculate_slope(x_initial, x_final, y_initial, y_final):
    return (y_final - y_initial) / (x_final - x_initial)    
