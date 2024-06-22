# DAT/EMI - Electronics and Microelectronics Department
# Redistribution, modification or use of this software in source or binary
# forms is permitted as long as the files maintain this copyright. 

###############################################################################
# DAT/EMI and the Brazilian Center for Research in Energy and Materials (CNPEM)
# are not liable for any misuse of this material.
#
# @file device_specific_commands.py
#
# @brief CLI for controlling OScilloscope, Wavegenerator and TestVector.
#
# @author Pedro Trindade 
# @author Eric Sonagli Abbade.
# @date 24/04/2024
###############################################################################

class ACCEPTED_FUNCTION_TYPES:
    sine = 'SINusoid' 
    square = 'SQUare'
    triangle = 'TRIangle'
    ramp = 'RAMP'
    pulse = 'PULSe'
    noise = 'NOIS'
    random_bits = 'PRBS'
    step = 'DC' 

class ACCEPTED_PRBS_DATA_TYPES:
    pn7 = 'PN7'
    pn9 = 'PN9'
    pn11 = 'PN11'
    pn15 = 'PN15'
    pn20 = 'PN20'
    pn23 = 'PN23'

class WRITE_COMMANDS:
    change_amplitude = ':SOURce{channel}:VOLTage {voltage}' 
    change_frequency = ':SOURce{channel}:FREQuency {frequency}'  
    change_offset = ':SOURce{channel}:VOLTage:OFFSet {offset_voltage}' 
    change_phase = ':SOURce{channel}:PHASe {phase}'  
    change_function_type =  ':SOURce{channel}:FUNCtion {function_type}' 
    change_duty_cycle = ':SOURce{channel}:FUNCtion:SQUare:DCYCle {duty_cycle}'
    change_symmetry = ':SOURce{channel}:FUNCtion:RAMP:SYMMetry {symmetry}'
    change_pulse_width = ':SOURce{channel}:FUNCtion:PULSe:WIDTh {pulse_width}'
    change_leading_edge = ':SOURce{channel}:FUNCtion:PULSe:TRANsition:LEADing {leading_edge}'
    change_trailing_edge = ':SOURce{channel}:FUNCtion:PULSe:TRANsition:TRAiling {trailing_edge}'
    change_noise_bandwidth = ':SOURce{channel}:FUNCtion:NOISe:BANDwidth {noise_bandwidth}'
    change_bit_rate = ':SOURce{channel}:FUNCtion:PRBS:BRATe {bit_rate}'
    change_edge_time = ':SOURce{channel}:FUNCtion:PRBS:TRANsition {edge_time}'
    change_prbs_data = ':SOURce{channel}:FUNCtion:PRBS:DATA {prbs_data}'
    change_output_on = ':OUTPut{channel} {output}' 
    change_output_off = ':OUTPut{channel} {output}'


class QUERY_COMMANDS:
    read_all = ':SOURce{channel}:APPLy?'
    read_amplitude = ':SOURce{channel}:VOLTage?'
    read_frequency = ':SOURce{channel}:FREQuency?' 
    read_offset = ':SOURce{channel}:VOLTage:OFFSet?' 
    read_phase = ':SOURce{channel}:PHASe?'
    read_function_type = ':SOURce{channel}:FUNCtion?'
    read_duty_cycle = ':SOURce{channel}:FUNCtion:SQUare:DCYCle?'
    read_symmetry = ':SOURce{channel}:FUNCtion:RAMP:SYMMetry?'
    read_pulse_width = ':SOURce{channel}:FUNCtion:PULSe:WIDTh?'
    read_leading_edge = ':SOURce{channel}:FUNCtion:PULSe:TRANsition:LEADing?'
    read_trailing_edge = ':SOURce{channel}:FUNCtion:PULSe:TRANsition:TRAiling?'
    read_noise_bandwidth = ':SOURce{channel}:FUNCtion:NOISe:BANDwidth?'
    read_bit_rate = ':SOURce{channel}:FUNCtion:PRBS:BRATe?'
    read_edge_time = ':SOURce{channel}:FUNCtion:PRBS:TRANsition?'
    read_prbs_data = ':SOURce{channel}:FUNCtion:PRBS:DATA?'
    read_output = ':OUTPut{channel}?'
    read_idn = '*IDN?'
    read_opt = '*OPT?'
    read_opc = '*OPC?'
   