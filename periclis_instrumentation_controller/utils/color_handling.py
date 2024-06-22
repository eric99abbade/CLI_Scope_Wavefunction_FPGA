
# DAT/EMI - Electronics and Microelectronics Department
# Redistribution, modification or use of this software in source or binary
# forms is permitted as long as the files maintain this copyright. 

###############################################################################
# DAT/EMI and the Brazilian Center for Research in Energy and Materials (CNPEM)
# are not liable for any misuse of this material.
#
# @file colors_handling.py
#
# @brief CLI for controlling OScilloscope, Wavegenerator and TestVector.
#
# @author Pedro Trindade 
# @author Eric Sonagli Abbade.
# @date 24/04/2024
###############################################################################

class COLORS:
    RED = "\001\033[91m\002"
    GREEN = "\001\033[92m\002"
    BLUE = "\001\033[94m\002"
    YELLOW = "\001\033[93m\002"
    CLEAR = "\001\033[0m\002"

def print_red(arg: str):
    print(get_red(arg))

def print_green(arg: str):
    print(get_green(arg))

def print_blue(arg: str):
    print(get_blue(arg))

def print_yellow(arg: str):
    print(get_yellow(arg))

def get_red(arg: str):
    return COLORS.RED + arg + COLORS.CLEAR

def get_green(arg: str):
    return COLORS.GREEN + arg + COLORS.CLEAR

def get_blue(arg: str):
    return COLORS.BLUE + arg + COLORS.CLEAR

def get_yellow(arg: str):
    return COLORS.YELLOW + arg + COLORS.CLEAR

def channel_color_selector(channel: int):
    if channel == 1:
        return 'c'
    elif channel == 2:
        return 'y'
    elif channel == 3:
        return 'pink'
    elif channel == 4:
        return 'g'
    else:
        return 'b'
