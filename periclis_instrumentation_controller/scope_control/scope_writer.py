# DAT/EMI - Electronics and Microelectronics Department
# Redistribution, modification or use of this software in source or binary
# forms is permitted as long as the files maintain this copyright. 


###############################################################################
# DAT/EMI and the Brazilian Center for Research in Energy and Materials (CNPEM)
# are not liable for any misuse of this material.
#
# @file scope_writer.py
#
# @brief CLI for controlling OScilloscope, Wavegenerator and TestVector.
#
# @author Pedro Trindade 
# @author Eric Sonagli Abbade.
# @date 24/04/2024
###############################################################################
from periclis_instrumentation_controller.scope_control.device_specific_commands import WRITE_COMMANDS, QUERY_COMMANDS, ACCEPTED_TRIGGER_TYPES, ACCEPTED_CHANNELS, ACCEPTED_TRIGGER_COUPLING, ACCEPTED_TRIGGER_SLOPE
from periclis_instrumentation_controller.scope_control.services_metainfo import SERVICES_METAINFO
from periclis_instrumentation_controller.scope_control.acquisitions_configurations import acquisitions_configurations
from periclis_instrumentation_controller.scope_control.controller_config import *
from periclis_instrumentation_controller.utils.decorators import service_add
from periclis_instrumentation_controller.utils.errors_handling import *
from periclis_instrumentation_controller.utils.file_parsing import *
import time

# A decorator facilitating listing services boilerplate
service = service_add(controller_name=CONTROLLER_NAME, 
                      services_metainfo=SERVICES_METAINFO)

class ScopeWriter(acquisitions_configurations):
    def __init__(self, scope_generator) -> None:
        self.scope_generator = scope_generator
        
    def _write(self, scope_command : str):
        self.scope_generator.write(scope_command)

    @service    
    def autoscale(self):               
        self._write(WRITE_COMMANDS.autoscale)
        print("Wait while autoscale is finished...")
        time.sleep(float(self.delay_autoscale))
        print("Autoscale time period finished")
    
    @service    
    def button_single(self): #Equals pressing Single button.         
        self._write(WRITE_COMMANDS.single)

    @service    
    def press_run_stop(self): #Equals pressing Run/Stop button.         
        self._write(WRITE_COMMANDS.run_stop)

    @service
    def default_configurations (self): 
        return_default_configurations(self, RESOURCE_DIR, DEFAULT_CONFIGURATIONS, FILE_NAME, INPUT_FORMAT, self.scope_generator, CONTROLLER_NAME)

    @service    
    def change_channel_on(self, channel:int=1): 
        channel = check_channels(channel, self.standard_channel) #Correct channel for its correct value. 
        channel = first_list_argument(channel, self.rounding_places)
        self._write(WRITE_COMMANDS.change_channel_on.format(channel=int(channel)))

    @service    
    def change_channel_off(self, channel:int=1): 
        channel = check_channels(channel, self.standard_channel) #Correct channel for its correct value. 
        channel = first_list_argument(channel, self.rounding_places)
        self._write(WRITE_COMMANDS.change_channel_off.format(channel=int(channel))) 
        
    @service
    def change_configuration (self, args):
        change_specific_configuration(self, args, RESOURCE_DIR, FILE_NAME, INPUT_FORMAT, self.scope_generator, CONTROLLER_NAME)
           
    @service
    def change_instrument_timeout(self, timeout_value):
        timeout_value = float(first_list_argument(timeout_value, int(self.rounding_places)))
        error_non_positive(timeout_value, "change_instrument_timeout", "timeout", int(self.rounding_places)) #Checks if the argument is non positive.
        self.scope_generator.timeout = (timeout_value*1000) #Changes the timeout to the desired value (s).
        
    @service    
    def change_probe_gain(self, gain, channel:int=1): #Changes the probe constant gain that multiplies the value read.
        try:
            channel = channel = gain[1]
        except:
            channel = 1 
        channel = check_channels(channel, self.standard_channel) #Correct channel for its correct value.  
        gain = first_list_argument(gain, self.rounding_places)
        error_negative(gain, "change_probe_gain", "gain", self.rounding_places) #Checks if the argument is negative.
        self._write(WRITE_COMMANDS.change_probe_gain.format(channel=channel, gain=1/(float(gain))))
    
    @service    
    def change_x_scale(self, scale_x): #This parameter equals the total horizontal length of the scope (in seconds).
        scale_x = first_list_argument(scale_x, int(self.rounding_places_time_scale))
        error_non_positive(scale_x, "change_scale_x", "scale_x", int(self.rounding_places_time_scale)) #Checks if the argument is non positive.
        self._write(WRITE_COMMANDS.change_scale_x.format(scale_x=float(scale_x)/(float(self.squares_x_axis))))
    
    @service    
    def change_y_scale(self, scale_y, channel:int=1): #This parameter equals the total vertical height of the scope (in Volts). 
        try:
            channel = scale_y[1]
        except:
            channel = 1        
        channel = check_channels(channel, self.standard_channel) #Correct channel for its correct value.        
        scale_y = first_list_argument(scale_y, self.rounding_places)
        error_non_positive(scale_y, "change_scale_y", "scale_y", self.rounding_places) #Checks if the argument is non positive.
        self._write(WRITE_COMMANDS.change_scale_y.format(channel=channel, scale_y=float(scale_y)/(float(self.squares_y_axis))))

    @service    
    def change_reference_level(self, position, channel:int=1): #This parameter equals the voltage level of a channel (in Volts). 
        try:
            channel = position[1]
        except:
            channel = 1
        channel = check_channels(channel, self.standard_channel) #Correct channel for its correct value. 
        position = first_list_argument(position, self.rounding_places)
        y_scale = float(self._query(QUERY_COMMANDS.read_scale_y.format(channel=channel))) #Y scale value of a channel square in Volts.
        self._write(WRITE_COMMANDS.change_reference_level.format(channel=channel, position=(position/y_scale)))
        
    @service
    def change_voltage_threshold_trigger(self, trigger_threshold):
        trigger_threshold = first_list_argument(trigger_threshold, self.rounding_places)
        error_negative(trigger_threshold, "change_trigger_threshold", "trigger_threshold", self.rounding_places) #Checks if the argument is negative.
        self._write(WRITE_COMMANDS.change_trigger_threshold.format(trigger_threshold=trigger_threshold)) 

    @service    
    def change_holdoff_trigger(self, trigger_holdoff):
        trigger_holdoff = first_list_argument(trigger_holdoff, self.rounding_places_holdoff)
        error_non_positive(trigger_holdoff, "change_trigger_holdoff", "trigger_holdoff", self.rounding_places_holdoff) #Checks if the argument is non positive.
        self._write(WRITE_COMMANDS.change_trigger_holdoff.format(trigger_holdoff=trigger_holdoff))
        
    @service
    def change_type_trigger(self, trigger_type):
        trigger_type = first_list_argument(trigger_type)
        check_list_options(trigger_type, dir(ACCEPTED_TRIGGER_TYPES), "change_trigger_type", "trigger_type")    
        self._write(WRITE_COMMANDS.change_trigger_type.format(trigger_type=getattr(ACCEPTED_TRIGGER_TYPES, 
                                                                                     trigger_type))) 
        
    @service
    def change_channel_trigger(self, trigger_channel):
        trigger_channel = first_list_argument(trigger_channel)
        check_list_options(trigger_channel, dir(ACCEPTED_CHANNELS), "change_trigger_channel", "trigger_channel")   
        self._write(WRITE_COMMANDS.change_trigger_channel.format(trigger_channel=getattr(ACCEPTED_CHANNELS, 
                                                                                     trigger_channel))) 
        
    @service
    def change_coupling_trigger(self, trigger_coupling):
        trigger_coupling = first_list_argument(trigger_coupling)
        check_list_options(trigger_coupling, dir(ACCEPTED_TRIGGER_COUPLING), "change_trigger_coupling", "trigger_coupling")
        self._write(WRITE_COMMANDS.change_trigger_coupling.format(trigger_coupling=getattr(ACCEPTED_TRIGGER_COUPLING, 
                                                                                     trigger_coupling))) 
        
    @service
    def change_slope_trigger(self, trigger_slope):
        trigger_slope = first_list_argument(trigger_slope)
        check_list_options(trigger_slope, dir(ACCEPTED_TRIGGER_SLOPE), "change_trigger_slope", "trigger_slope")
        self._write(WRITE_COMMANDS.change_trigger_slope.format(trigger_slope=getattr(ACCEPTED_TRIGGER_SLOPE, 
                                                                                     trigger_slope)))        
    @service
    def use_trigger_mode(self, configurated:list=0, scale:int=0, channel:int=1):
        try:
            scale = configurated[1]
        except:
            scale = 0 
        try:
            channel = configurated[2]
        except:
            channel = self.channel_std_trigger        
        configurated = int(first_list_argument(configurated, self.rounding_places))
        acquisitions_configurations.__init__(self, True, configurated, scale, channel)
   

"""
useful link:
https://www.linkedin.com/pulse/accessing-querying-data-from-oscilloscope-pyvisa-yamil-garcia-pclye
"""