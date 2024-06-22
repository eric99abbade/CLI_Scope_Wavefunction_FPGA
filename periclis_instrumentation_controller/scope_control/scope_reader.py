# DAT/EMI - Electronics and Microelectronics Department
# Redistribution, modification or use of this software in source or binary
# forms is permitted as long as the files maintain this copyright. 

###############################################################################
# DAT/EMI and the Brazilian Center for Research in Energy and Materials (CNPEM)
# are not liable for any misuse of this material.
#
# @file scope_reader.py
#
# @brief CLI for controlling OScilloscope, Wavegenerator and TestVector.
#
# @author Pedro Trindade 
# @author Eric Sonagli Abbade.
# @date 24/04/2024
###############################################################################

from periclis_instrumentation_controller.utils.decorators import service_add
from periclis_instrumentation_controller.scope_control.device_specific_commands import QUERY_COMMANDS, READ_SCALE_CURVE_GENERATOR
from periclis_instrumentation_controller.scope_control.acquisitions_configurations import acquisitions_configurations
from periclis_instrumentation_controller.scope_control.controller_config import *
from periclis_instrumentation_controller.utils.errors_handling import *
from periclis_instrumentation_controller.utils.color_handling import *
from periclis_instrumentation_controller.utils.file_parsing import *
from periclis_instrumentation_controller.utils.data_conversion import *

# A decorator facilitating listing services boilerplate
service = service_add(controller_name=CONTROLLER_NAME)

# This Python class, `scopeInfoReader`, provides methods to query and read scope information
# from a scope generator.
class ScopeReader(acquisitions_configurations):
    def __init__(self, scope_generator) -> None:
        self.scope_generator = scope_generator
        
    def _query(self, query_string : str):
        return self.scope_generator.query(query_string)
    
    @service
    def read_default_configurations(self):
        print_configurations(RESOURCE_DIR, DEFAULT_CONFIGURATIONS, INPUT_FORMAT)   
    
    @service
    def read_configurations(self):
        print_configurations(RESOURCE_DIR, FILE_NAME, INPUT_FORMAT)              
    
    @service
    def read_channel_state(self, channel:int=1):
        channel = check_channels(channel, self.standard_channel) #Correct channel for its correct value. 
        channel = first_list_argument(channel, self.rounding_places)
        convert_binary_on_off(self._query(QUERY_COMMANDS.read_channel_state.format(channel=int(channel))))
        #return result
    
    @service
    def read_state_trigger(self):
        result = self._query(QUERY_COMMANDS.read_trigger_state.format())
        print_green(result)  
        #return result
    
    """
    #These services are mostly useful only for the activity of saving images (for which they are already being used).
    #Hence, in order to maintain the CLI usability, these services will be commented. If needed, uncomment them!

    @service
    def read_wfm_record_scale(self):
        result = self._query(QUERY_COMMANDS.read_scale_wfm_record.format())  
        print_green(result)  
        #return result
    
    @service
    def read_pre_trig_record_scale(self):
        result = self._query(QUERY_COMMANDS.read_scale_pre_trig_record.format())  
        print_green(result)  
        #return result
    
    @service
    def read_t_scale(self):
        result = self._query_scale(QUERY_COMMANDS.read_scale_t.format())  
        print_green(result)  
        #return result
    
    @service
    def read_t_sub_scale(self):
        result = self._query(QUERY_COMMANDS.read_scale_t_sub.format())  
        print_green(result)  
        #return result
    
    @service
    def read_v_scale(self):
        result = self._query(QUERY_COMMANDS.read_scale_v.format())  
        print_green(result)  
        #return result
    
    @service
    def read_v_off_scale(self):
        result = self._query(QUERY_COMMANDS.read_scale_v_off.format())  
        print_green(result)  
        #return result
    
    @service
    def read_v_pos_scale(self):
        result = self._query(QUERY_COMMANDS.read_scale_v_pos.format())  
        print_green(result)  
        #return result
    """
    
    @service
    def read_instrument_timeout(self):
        result = str(float(self.scope_generator.timeout)/1000)
        print_green(result)
    
    @service    
    def read_probe_gain(self, channel:int=1): #Reads the probe constant gain that multiplies the value read.
        channel = check_channels(channel, self.standard_channel) #Correct channel for its correct value.  
        result = str(1/float(self._query(QUERY_COMMANDS.read_probe_gain.format(channel=channel))))
        print_green(result)
    
    @service    
    def read_x_scale(self): #This parameter equals the total horizontal length of the scope (in seconds).
        result = str(float(self._query(QUERY_COMMANDS.read_scale_x.format()))*float(self.squares_x_axis))
        print_green(result)
    
    @service    
    def read_y_scale(self, channel:int=1): #This parameter equals the total vertical height of the scope (in Volts). 
        channel = check_channels(channel, self.standard_channel) #Correct channel for its correct value.        
        result = str(float(self._query(QUERY_COMMANDS.read_scale_y.format(channel=channel)))*float(self.squares_y_axis))
        print_green(result)

    @service    
    def read_reference_level(self, channel:int=1): #This parameter equals the voltage level of a channel (in Volts). 
        channel = check_channels(channel, self.standard_channel) #Correct channel for its correct value. 
        y_scale = float(self._query(QUERY_COMMANDS.read_scale_y.format(channel=channel))) #Y scale value of a channel square in Volts.
        result = str(float(self._query(QUERY_COMMANDS.read_reference_level.format(channel=channel)))*y_scale)
        print_green(result)

    @service
    def read_voltage_threshold_trigger(self):
        result = self._query(QUERY_COMMANDS.read_trigger_threshold.format())  
        print_green(result)  
        #return result
    
    @service
    def read_holdoff_trigger(self):
        result = self._query(QUERY_COMMANDS.read_trigger_holdoff.format())  
        print_green(result)  
        #return result
    
    @service
    def read_type_trigger(self):
        result = self._query(QUERY_COMMANDS.read_trigger_type.format())  
        print_green(result)  
        #return result

    @service
    def read_channel_trigger(self):
        result = self._query(QUERY_COMMANDS.read_trigger_channel.format())  
        print_green(result)  
        #return result

    @service
    def read_coupling_trigger(self):
        result = self._query(QUERY_COMMANDS.read_trigger_coupling.format())  
        print_green(result)  
        #return result
    
    @service
    def read_slope_trigger(self):
        result = self._query(QUERY_COMMANDS.read_trigger_slope.format())  
        print_green(result)  
        #return result
    
    @service    
    def monitore_dc_voltage(self, channel:int=1): #Continuous voltage monitoring.  
        channel = check_channels(channel, self.standard_channel) #Correct channel for its correct value. 
        self.trigger_use = False #Variable for not plot with threshold.
        acquisitions_configurations.__init__(self, False, 1, 1, channel)
        result = str((sum(self.scaled_wave) / len(self.scaled_wave)))
        print_green("Voltage (Volts): " + result)

    



     

    