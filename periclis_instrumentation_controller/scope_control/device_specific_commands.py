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

class ACCEPTED_TRIGGER_TYPES:
    edge = 'EDGe' 
    logic = 'LOGic'
    pulse = 'PULSe'
    bus = 'BUS'
    video = 'VIDeo'

class ACCEPTED_CHANNELS:
    ch1 = 'CH1' 
    ch2 = 'CH2'
    ch3 = 'CH3'
    ch4 = 'CH4'
    
class ACCEPTED_TRIGGER_COUPLING:
    dc = 'DC' 
    hf = 'HFR'
    lf = 'LFR'
    noise = 'NOISE'

class ACCEPTED_TRIGGER_SLOPE:
    rise = 'RISE'
    fall = 'FALL'


class WRITE_COMMANDS:      
    autoscale = 'AUTOSET EXECute' #Autoscale.   
    single = 'FPANEL:PRESS SINGleseq' #Equals pressing Single button.   
    run_stop = 'FPANEL:PRESS RUnstop' #Equals pressing Run/Stop button.   
    change_channel_on = 'SELECT:CH{channel} ON' #Turns the channel on.  
    change_channel_off = 'SELECT:CH{channel} OFF' #Turns the channel off. 
    change_probe_gain = 'CH{channel}:PRObe:GAIN {gain}'
    change_scale_x = 'HORizontal:MAIn:SCAle {scale_x}'
    change_scale_y = 'CH{channel}:SCAle {scale_y}'
    change_reference_level = 'CH{channel}:POSition {position}'
    change_trigger_threshold = 'TRIGGER:A:LEVEL {trigger_threshold}' #Defines the voltage threshold of trigger.
    change_trigger_holdoff = 'TRIGGER:A:HOLDOFF:TIME {trigger_holdoff}' #Defines the holdoff time of the trigger.
    change_trigger_type = 'TRIGger:A:TYPe {trigger_type}' #Defines the type of the trigger: EDGe, LOGic, PULSe, BUS or VIDeo.
    change_trigger_channel = 'TRIGGER:A:EDGE:SOURCE {trigger_channel}' #Defines the channel of the trigger: CH1, CH2, CH3, or CH4.
    change_trigger_coupling = 'TRIGGER:A:EDGE:COUPLING {trigger_coupling}' #Defines the coupling of the trigger: DC, HFR, LFR, or NOISE.
    change_trigger_slope = 'TRIGGER:A:EDGE:SLOPE {trigger_slope}' #Defines the coupling of the slope: RISE, or FALL.
    
    
    

class QUERY_COMMANDS:
    read_channel_state = 'SELECT:CH{channel}?' #Returns if the channel is on or off.   
    read_trigger_state = 'TRIGger:STATE?' #Returns the state of the trigger: ARMED, AUTO, READY, SAVE or TRIGGER.
    read_scale_wfm_record = 'wfmoutpre:nr_pt?' 
    read_scale_pre_trig_record = 'wfmoutpre:pt_off?'
    read_scale_t = 'wfmoutpre:xincr?'
    read_scale_t_sub = 'wfmoutpre:xzero?'
    read_scale_v = 'wfmoutpre:ymult?'
    read_scale_v_off = 'wfmoutpre:yzero?'
    read_scale_v_pos = 'wfmoutpre:yoff?'
    read_probe_gain = 'CH{channel}:PRObe:GAIN?'
    read_scale_x = 'HORizontal:MAIn:SCAle?'
    read_scale_y = 'CH{channel}:SCAle?'
    read_reference_level = 'CH{channel}:POSition?'
    read_trigger_threshold = 'TRIGger:A:LEVel?' #Returns the voltage level that activates trigger in Volts (example: 0.04 = 40mV)
    read_trigger_holdoff = 'TRIGGER:A:HOLDOFF:TIME?' #Returns the holdoff time (period during which the trigger will not generate a trigger event, in seconds).
    read_trigger_type = 'TRIGger:A:TYPe?' #Returns the type of the trigger: EDGe, LOGic, PULSe, BUS or VIDeo.
    read_trigger_channel = 'TRIGGER:A:EDGE:SOURCE?' #Returns the channel of the trigger (example: CH1).
    read_trigger_coupling = 'TRIGGER:A:EDGE:COUPLING?' #Returns the coupling of the trigger: DC, High Frequency(HF) Reject, Low Frequency(LF) Reject or Noise Reject.
    read_trigger_slope = 'TRIGGER:A:EDGE:SLOPE?' #Returns the trigger slope (rising or falling edge).

    
    
class WRITE_ACQUISITION:
    change_acquisition_encdg = 'data:encdg {acquisition_encdg}' 
    change_acquisition_channel = 'data:source {acquisition_channel}'
    change_acquisition_start = 'data:start {acquisition_start}'    
    change_acquisition_stop = 'data:stop {acquisition_stop}'
    change_acquisition_byt_n = 'wfmoutpre:byt_n {acquisition_byt_n}'



class READ_SCALE_CURVE_GENERATOR:
    read_scale_wfm_record = 'wfmoutpre:nr_pt?'
    read_scale_pre_trig_record = 'wfmoutpre:pt_off?'
    read_scale_t = 'wfmoutpre:xincr?'
    read_scale_t_sub = 'wfmoutpre:xzero?'
    read_scale_v = 'wfmoutpre:ymult?'
    read_scale_v_off = 'wfmoutpre:yzero?'
    read_scale_v_pos = 'wfmoutpre:yoff?'
    read_acquisition_horizontal = 'horizontal:recordlength?'
