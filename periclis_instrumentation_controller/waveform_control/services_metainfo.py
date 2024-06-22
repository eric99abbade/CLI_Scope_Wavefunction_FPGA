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
from periclis_instrumentation_controller.waveform_control.device_specific_commands import WRITE_COMMANDS, ACCEPTED_FUNCTION_TYPES, ACCEPTED_PRBS_DATA_TYPES
from periclis_instrumentation_controller.cli.str_formatting import function_checker


SERVICES_METAINFO = {
   "change_instrument_timeout": {
       "args": {"Timeout to be waited until communication finishes (s).": None}
       },
   "change_amplitude": {
       "args": {"voltage (V)": None}
       },
    "change_frequency": {
       "args": {"frequency (Hz)": None}
       },
    "change_voltage_offset": {
       "args": {"offset (V)": None}
       },
    "change_phase": {
       "args": {"phase in degrees (°)": None}
       },
    "change_duty_cycle": {
       "args": {"duty cycle (%) - specific of square wave type": None}
       },
    "change_symmetry": {
       "args": {"symmetry (%) - specific of ramp wave type": None}
       },
    "change_pulse_width": {
       "args": {"pulse width (s) - specific of pulse wave type": None}
       },
    "change_leading_edge": {
       "args": {"lead edge (s) - specific of pulse wave type": None}
       },
    "change_trailing_edge": {
       "args": {"trail edge (s) - specific of pulse wave type": None}
       },
    "change_noise_bandwidth": {
       "args": {"bandwidth (Hz) - specific of noise wave type": None}
       },
    "change_bit_rate": {
       "args": {"bit rate per second (bps) - specific of PRBS wave type": None}
       },
    "change_edge_time": {
       "args": {"edge time (s) - specific of PRBS wave type": None}
       },
    "change_prbs_data": {
       "args": {"prbs data - specific of PRBS wave type": function_checker(dir(ACCEPTED_PRBS_DATA_TYPES))}
       },
    "change_configuration": {
         "args": {'configuration_name, configuration_value': None}
       },
    "change_function_type": {
       "args": {"Type of the function, examples:": function_checker(dir(ACCEPTED_FUNCTION_TYPES))}
    }
}
