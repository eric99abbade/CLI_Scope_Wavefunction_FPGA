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

#Arguments for error functions:

errors_arguments_mapping = {    
    'error_non_numerical': ("argument_value", "command", "argument", "rounding_places"), 
    'error_negative': ("argument_value", "command", "argument", 'rounding_places'),
    'error_non_positive': ("argument_value", "command", "argument", "rounding_places"),
    'error_interval': ("argument_value", "minimum", "maximum","command", "argument", 'rounding_places'),  
    'error_excludent_interval': ("argument_value", "minimum", "maximum", "command", "argument", "rounding_places"),  
    'check_list_options': ("argument_value", "accepted_list", "command", "argument", "rounding_places") 
}
