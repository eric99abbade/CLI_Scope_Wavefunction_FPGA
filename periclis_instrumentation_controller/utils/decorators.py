# DAT/EMI - Electronics and Microelectronics Department
# Redistribution, modification or use of this software in source or binary
# forms is permitted as long as the files maintain this copyright. 

###############################################################################
# DAT/EMI and the Brazilian Center for Research in Energy and Materials (CNPEM)
# are not liable for any misuse of this material.
#
# @file decorators.py
#
# @brief CLI for controlling OScilloscope, Wavegenerator and TestVector.
#
# @author Pedro Trindade 
# @author Eric Sonagli Abbade.
# @date 24/04/2024
###############################################################################

_SERVICES_DICT = {}

# This is a decorator to symbolize a method is a service
# and add to a predefined dict
def service_add(controller_name : str, services_metainfo : dict={}):
    # Adds the controller name to the services data
    if controller_name not in _SERVICES_DICT.keys():
        _SERVICES_DICT[controller_name] = {}
    
    def inner(func):
        _SERVICES_DICT[controller_name][func.__name__] = services_metainfo.get(func.__name__)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            return result
        
        return wrapper
    return inner
     
def get_services(controler_name : str) -> dict:
    return _SERVICES_DICT.get(controler_name)

# This returns a function that gets the arguments of 
# another function that prints the output
def service2print(func):
    def print_service(*args, **kwargs):
        print(func(*args, **kwargs))
    return print_service