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

#Classes with variable configurations of each controller and a function corresponding to a restriction of them.
class WaveformController_Configurations:
    standard_channel = 'error_non_positive'
    rounding_places = 'error_non_positive'
    rounding_places_configurations = 'error_non_positive'
    rounding_places_pulse_width = 'error_non_positive'
    rounding_places_pulse_edges = 'error_non_positive' 
    standard_timeout = 'error_non_positive'
 
class ScopeController_Configurations:
    standard_channel = 'error_non_positive'
    voltage_scale = 'error_non_positive'
    time_scale = 'error_non_positive'
    standard_timeout = 'error_non_positive'
    rounding_places = 'error_non_positive'
    rounding_places_configurations = 'error_non_positive'
    rounding_places_holdoff = 'error_non_positive'
    rounding_places_time_scale = 'error_non_positive'
    rounding_places_time_acquisition = 'error_non_positive'
    rounding_places_voltage_acquisition = 'error_non_positive'
    delay_check_wave = 'error_non_positive'
    delay_scale = 'error_non_positive'
    delay_autoscale = 'error_non_positive'
    delay_acquisition = 'error_non_positive'
    delay_single_pressing = 'error_non_positive'
    delay_general_commands = 'error_non_positive'
    tentatives_single_activating = 'error_non_positive'
    acquisitions_retries = 'error_non_positive'
    number_channels = 'error_non_positive'
    type_std_trigger = 'check_list_options', 'ACCEPTED_TRIGGER_TYPES'
    channel_std_trigger = 'error_non_positive'    
    coupling_std_trigger = 'check_list_options', 'ACCEPTED_TRIGGER_COUPLING'
    slope_std_trigger = 'check_list_options', 'ACCEPTED_TRIGGER_SLOPE'
    threshold_std_trigger = 'error_negative'
    holdoff_std_trigger = 'error_non_positive'
    squares_x_axis = 'error_non_positive'
    squares_y_axis = 'error_non_positive'
    probe_gain = 'error_non_positive'
    reference_level = 'error_non_numerical'
    add_channel_trigger_plot_1 = 'error_non_positive'
    add_channel_trigger_plot_2 = 'error_non_positive'
    add_channel_trigger_plot_3 = 'error_non_positive'

class TestVectorController_Configurations:
    vpp_voltage = 'error_negative'
    threshold_voltage = 'error_non_positive'
    voltage_offset = 'error_non_numerical'
    bits_resolution = 'error_non_positive'
    rounding_places_configurations = 'error_non_positive'
    signed = 'first_list_argument' #Boolean variable: it is already tested if the new variable is boolean.
    fractional_repr = 'error_non_positive'
    number_inputs = 'error_non_positive'
    number_samples = 'error_non_positive'
    sampling_period = 'error_non_positive'
    wave_type = 'check_list_options', 'ACCEPTED_WAVE_TYPE'
    frequency = 'error_non_positive'
    symmetry = 'error_interval', 0, 1
    duty_cycle = 'error_interval', 0, 100
    pulse_width = 'error_non_positive'
    lead_edge = 'error_non_positive'
    trail_edge = 'error_non_positive'
    symmetric_threshold = 'first_list_argument' #Boolean variable: it is already tested if the new variable is boolean.