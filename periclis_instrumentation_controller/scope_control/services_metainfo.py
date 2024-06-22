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

from periclis_instrumentation_controller.scope_control.device_specific_commands import WRITE_COMMANDS, ACCEPTED_TRIGGER_TYPES, ACCEPTED_CHANNELS, ACCEPTED_TRIGGER_COUPLING, ACCEPTED_TRIGGER_SLOPE
from periclis_instrumentation_controller.cli.str_formatting import function_checker

SERVICES_METAINFO = {
   "change_type_trigger": {
       "args": {"Type, examples:": function_checker(dir(ACCEPTED_TRIGGER_TYPES))}
       },
    "change_channel_trigger": {
       "args": {"Source (channel), examples:": function_checker(dir(ACCEPTED_CHANNELS))}
       },
    "change_coupling_trigger": {
       "args": {"Coupling, examples:": function_checker(dir(ACCEPTED_TRIGGER_COUPLING))}
       },
    "change_slope_trigger": {
       "args": {"Slope, examples:": function_checker(dir(ACCEPTED_TRIGGER_SLOPE))}
       },
    "change_voltage_threshold_trigger": {
       "args": {"Voltage threshold(V) (Scale must allow the threshold! Only multiples of 40 mV in some Scopes)": None}
       },
    "change_holdoff_trigger": {
       "args": {"Holdoff Time(s)": None}
       },   
    "change_instrument_timeout": {
       "args": {"Timeout to be waited until communication finishes (s).": None}
       },
    "change_probe_gain": {
       "args": {"Gain of the probe that multiplies the value read.": None}
       },
    "change_x_scale": {
         "args": {'Trigger horizontal scale (value of the scope full screen x-axis in seconds)': None}
       },
    "change_y_scale": {
         "args": {'Trigger vertical scale (value of the scope full screen y-axis in Volts)': None}
       },
    "change_reference_level": {
         "args": {'Voltage level position (reference value in Volts "0 V" according to full screen y-axis scale)': None}
       }, 
    "change_configuration": {
         "args": {'configuration_name, configuration_value': None}
       },
    "use_trigger_mode": {
         "args": {'Configurations (0:scope_config.csv / 1:scope), Scale (0:scope_config.csv / 1:scope / 2:autoscale).': 'Default:(0, 0)'}
       }
}