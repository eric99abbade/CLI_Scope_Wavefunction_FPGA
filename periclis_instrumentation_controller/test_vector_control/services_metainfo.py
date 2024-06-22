# DAT/EMI - Electronics and Microelectronics Department
# Redistribution, modification or use of this software in source or binary
# forms is permitted as long as the files maintain this copyright. 

###############################################################################
# DAT/EMI and the Brazilian Center for Research in Energy and Materials (CNPEM)
# are not liable for any misuse of this material.
#
# @file services_metainfo.py
#
# @brief CLI for controlling OScilloscope, Wavegenerator and TestVector.
#
# @author Pedro Trindade 
# @author Eric Sonagli Abbade.
# @date 24/04/2024
###############################################################################

SERVICES_METAINFO = {    
   "new_resource": {
       "args": {"json_file_name (.txt or .json)": None}
       },
    "delete_resource": {
       "args": {"json_file_name_to_delete": None}
       },
    "change_resource_config": {
       "args": {"configuration_variable_name, configuration_variable_new_value": None}
       },
    "copy_resource": {
       "args": {"json_file_name_to_receive_resource_copy": None}
       },
   "save_testvector": {
       "args": {"out_file_name (opt)": None}
       },
    "delete_testvector": {
         "args": {"file_name_to_delete": None}
    }
}