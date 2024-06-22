# DAT/EMI - Electronics and Microelectronics Department
# Redistribution, modification or use of this software in source or binary
# forms is permitted as long as the files maintain this copyright. 

###############################################################################
# DAT/EMI and the Brazilian Center for Research in Energy and Materials (CNPEM)
# are not liable for any misuse of this material.
#
# @file waveform_reader.py
#
# @brief CLI for controlling OScilloscope, Wavegenerator and TestVector.
#
# @author Pedro Trindade 
# @author Eric Sonagli Abbade.
# @date 24/04/2024
###############################################################################

from periclis_instrumentation_controller.waveform_control.device_specific_commands import QUERY_COMMANDS
from periclis_instrumentation_controller.waveform_control.controller_config import *
from periclis_instrumentation_controller.utils.decorators import service_add
from periclis_instrumentation_controller.utils.color_handling import *
from periclis_instrumentation_controller.utils.data_conversion import *
from periclis_instrumentation_controller.utils.file_parsing import *


# A decorator facilitating listing services boilerplate
service = service_add(controller_name=CONTROLLER_NAME)

# This Python class, `WaveformInfoReader`, provides methods to query and read waveform information
# from a waveform generator.
class WaveformInfoReader:
    def __init__(self, waveform_generator) -> None:
        self.waveform_generator = waveform_generator
        
    
    def _query(self, query_string : str):
        """
        This function takes a query string as input and calls the query method of the waveform_generator
        object with that query string.
        
        @param query_string The `query_string` parameter in the `query` method is a string that
        represents the query you want to send to the waveform generator. This string typically contains
        commands or instructions that the waveform generator will interpret and execute.
        
        @return The `query` method is returning the result of calling the `query` method of the
        `waveform_generator` object with the `query_string` parameter.
        """
        return self.waveform_generator.query(query_string)

    @service
    def read_default_configurations(self):
        print_configurations(RESOURCE_DIR, DEFAULT_CONFIGURATIONS, INPUT_FORMAT)   
    
    @service
    def read_configurations(self):
        print_configurations(RESOURCE_DIR, FILE_NAME, INPUT_FORMAT)
    
    @service
    def query_info(self, arg=None):
        """
        The `query_info` function retrieves configuration information by querying specific commands.
        
        @return The `query_info` method is returning a concatenated string of the results of querying three
        commands: '*IDN?', '*OPT?', and '*OPC?'.
        """
        some_config_info = self._query('*IDN?') + self._query('*OPT?') \
                   + self._query('*OPC?')

        print_green(some_config_info)
        #return some_config_info

    @service
    def read_instrument_timeout(self):
        result = str(float(self.waveform_generator.timeout)/1000)
        print_green(result)
    
    @service
    def read_type_frequency_amplitude_offset(self, channel: int = 1):
        """
        This function reads and returns the current settings of a waveform generator.
        
        @return The `read_all` method is returning the result of querying the instrument for the current
        settings of the waveform format, frequency (Hz), amplitude (V), and offset (V) for source 1
        before any editing of these parameters.
        """
        result = self._query(QUERY_COMMANDS.read_all.format(channel=channel))  #Leitura do formato de onda, frequência(Hz), amplitude(V) e offset(V), atuais, antes da edição desses parâmetros.
        print_green(result)
        #return result
    
    @service
    def read_output(self, channel: int = 1):
        """
        This Python function reads the function type of a source.
        
        @return The `read_function_type` function is returning the result of querying the function type
        of the source at index 1.
        """
        convert_binary_on_off(str(self._query(QUERY_COMMANDS.read_output.format(channel=1))))                
        #return result
    
    @service
    def read_amplitude(self, channel: int = 1):
        """
        The function `read_voltage` queries the voltage value from a specified source in a Python script.
        
        @return The `read_voltage` function is returning the voltage value queried from the instrument
        with the command `:SOURce1:VOLTage?`.
        """
        result = self._query(QUERY_COMMANDS.read_amplitude.format(channel=channel)) 
        print_green(result) 
        #return result

    @service
    def read_frequency(self, channel: int = 1):
        """
        The function `read_frequency` queries and returns the frequency of a source in a Python program.
        
        @return The `read_frequency` method is returning the frequency value of the source specified by
        `:SOURce1:FREQuency?`.
        """
        result = self._query(QUERY_COMMANDS.read_frequency.format(channel=channel))  
        print_green(result)
        #return result

    @service
    def read_voltage_offset(self, channel: int =1):
        """
        The `read_offset` function reads the voltage offset value for a specific source in Python.
        
        @return The `read_offset` method is returning the voltage offset value for the source 1.
        """
        result = self._query(QUERY_COMMANDS.read_offset.format(channel=channel))  
        print_green(result)
        #return result
    
    @service
    def read_phase(self, channel: int = 1):
        """
        This Python function reads the phase value of a specified source.
        
        @return The `read_phase` method is returning the phase value of the specified source channel
        (channel 1 in this case) by querying the instrument using the command `:SOURce1:PHASe?`. The
        result of this query is then returned by the method.
        """
        result = self._query(QUERY_COMMANDS.read_phase.format(channel=channel))  
        print_green(result)
        #return result

    @service
    def read_duty_cycle(self, channel: int = 1):
        result = self._query(QUERY_COMMANDS.read_duty_cycle.format(channel=channel))  
        print_green(result)
        #return result

    @service
    def read_symmetry(self, channel: int = 1):
        result = self._query(QUERY_COMMANDS.read_symmetry.format(channel=channel))  
        print_green(result)
        #return result
        
    @service
    def read_pulse_width(self, channel: int = 1):
        result = self._query(QUERY_COMMANDS.read_pulse_width.format(channel=channel))  
        print_green(result)
        #return result

    @service
    def read_leading_edge(self, channel: int = 1):
        result = self._query(QUERY_COMMANDS.read_leading_edge.format(channel=channel))  
        print_green(result)
        #return result

    @service
    def read_trailing_edge(self, channel: int = 1):
        result = self._query(QUERY_COMMANDS.read_trailing_edge.format(channel=channel))  
        print_green(result)
        #return result

    @service
    def read_noise_bandwidth(self, channel: int = 1):
        result = self._query(QUERY_COMMANDS.read_noise_bandwidth.format(channel=channel))  
        print_green(result)
        #return result
    
    @service
    def read_bit_rate (self, channel: int = 1):
        result = self._query(QUERY_COMMANDS.read_bit_rate.format(channel=channel))  
        print_green(result)
        #return result

    @service
    def read_edge_time (self, channel: int = 1):
        result = self._query(QUERY_COMMANDS.read_edge_time.format(channel=channel))  
        print_green(result)
        #return result

    @service
    def read_prbs_data(self, channel: int = 1):
        result = self._query(QUERY_COMMANDS.read_prbs_data.format(channel=channel))  
        print_green(result)
        #return result
    
    @service
    def read_function_type(self, channel: int = 1):
        """
        This Python function reads the function type of a source.
        
        @return The `read_function_type` function is returning the result of querying the function type
        of the source at index 1.
        """
        result = self._query(QUERY_COMMANDS.read_function_type.format(channel=channel))  
        print_green(result)
        #return result

    

   
