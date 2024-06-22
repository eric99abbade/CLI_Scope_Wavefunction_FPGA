# DAT/EMI - Electronics and Microelectronics Department
# Redistribution, modification or use of this software in source or binary
# forms is permitted as long as the files maintain this copyright. 

###############################################################################
# DAT/EMI and the Brazilian Center for Research in Energy and Materials (CNPEM)
# are not liable for any misuse of this material.
#
# @file waveform_writer.py
#
# @brief CLI for controlling OScilloscope, Wavegenerator and TestVector.
#
# @author Pedro Trindade 
# @author Eric Sonagli Abbade.
# @date 24/04/2024
###############################################################################

from periclis_instrumentation_controller.waveform_control.device_specific_commands import WRITE_COMMANDS, ACCEPTED_FUNCTION_TYPES, ACCEPTED_PRBS_DATA_TYPES
from periclis_instrumentation_controller.waveform_control.services_metainfo import SERVICES_METAINFO
from periclis_instrumentation_controller.waveform_control.controller_config import *
from periclis_instrumentation_controller.utils.decorators import service_add
from periclis_instrumentation_controller.utils.errors_handling import *
from periclis_instrumentation_controller.utils.file_parsing import *
from periclis_instrumentation_controller.cli.execute_visa_commands import visa_read, visa_write

# A decorator facilitating listing services boilerplate
service = service_add(controller_name=CONTROLLER_NAME, 
                      services_metainfo=SERVICES_METAINFO)

class WaveformWriter:
    def __init__(self, waveform_generator) -> None:
        self.waveform_generator = waveform_generator
        
                
    def _write(self, waveform_command : str):
        self.waveform_generator.write(waveform_command)
    
    @service
    def default_configurations (self): 
        return_default_configurations(self, RESOURCE_DIR, DEFAULT_CONFIGURATIONS, FILE_NAME, INPUT_FORMAT, self.waveform_generator, CONTROLLER_NAME)  

    @service
    def change_output_on(self, channel : int = 1):
        channel = first_list_argument(int(channel), self.rounding_places)      
        channel = int(channel)
        self._write(WRITE_COMMANDS.change_output_on.format(channel=channel, output=1)) #Turning output on.
        
    @service
    def change_output_off(self, channel : int = 1):
        channel = first_list_argument(int(channel), self.rounding_places)      
        channel = int(channel)  
        self._write(WRITE_COMMANDS.change_output_off.format(channel=channel, output=0)) #Turning output on.

    @service
    def change_instrument_timeout(self, timeout_value):
        timeout_value = float(first_list_argument(timeout_value, int(self.rounding_places)))
        error_non_positive(timeout_value, "change_instrument_timeout", "timeout", int(self.rounding_places)) #Checks if the argument is non positive.
        self.waveform_generator.timeout = (timeout_value*1000) #Changes the timeout to the desired value (s).

    @service
    def change_amplitude(self, amplitude : float, channel : int = 1):
        amplitude = first_list_argument(amplitude, self.rounding_places)
        error_non_positive(amplitude, "change_amplitude", "voltage", self.rounding_places) #Checks if the argument is non positive.
        self._write(WRITE_COMMANDS.change_amplitude.format(channel=channel, voltage=amplitude)) #Amplitude (in V).

    @service
    def change_frequency(self, freq_hz, channel : int = 1):
        freq_hz = first_list_argument(freq_hz, self.rounding_places)
        error_non_positive(freq_hz, "change_frequency", "frequency", self.rounding_places) #Checks if the argument is non positive.
        self._write(WRITE_COMMANDS.change_frequency.format(channel=channel, frequency=freq_hz)) #Frequency (in Hz).

    @service
    def change_voltage_offset(self, offset_value, channel : int = 1):
        offset_value = first_list_argument(offset_value, self.rounding_places)
        error_non_numerical(offset_value, "change_offset", "offset", self.rounding_places) #Checks if the argument is numeric.
        self._write(WRITE_COMMANDS.change_offset.format(channel=channel, offset_voltage=offset_value)) #Offset (in V.) Average value of the sinusoid and DC value are: 2*OFFSet.
    
    @service
    def change_phase(self, phase_value, channel : int = 1):
        phase_value = first_list_argument(phase_value, self.rounding_places)
        error_interval(phase_value, 0, 360, "change_phase", "phase", self.rounding_places) #Checks if the argument is in the interval.
        self._write(WRITE_COMMANDS.change_phase.format(channel=channel, phase=phase_value)) #Value from 0º to 360º.

    @service
    def change_duty_cycle(self, duty_cycle, channel : int = 1):
        duty_cycle = first_list_argument(duty_cycle, self.rounding_places)
        error_interval(duty_cycle, 0, 100, "change_duty_cycle", "duty_cycle", self.rounding_places) #Checks if the argument is in the interval.
        self._write(WRITE_COMMANDS.change_duty_cycle.format(channel=channel, duty_cycle=duty_cycle)) #Value from 0 to 100%.
    
    @service
    def change_symmetry(self, symmetry, channel : int = 1):
        symmetry = first_list_argument(symmetry, self.rounding_places)
        error_interval(symmetry, 0, 100, "change_symmetry", "symmetry", self.rounding_places) #Checks if the argument is in the interval.
        self._write(WRITE_COMMANDS.change_symmetry.format(channel=channel, symmetry=symmetry)) #Value from 0 to 100%.

    @service
    def change_pulse_width(self, pulse_width, channel : int = 1):
        pulse_width = first_list_argument(pulse_width, self.rounding_places_pulse_width)
        error_non_numerical(pulse_width, "change_pulse_width", "pulse_width", self.rounding_places_pulse_width) #Checks if the argument is numeric.
        self._write(WRITE_COMMANDS.change_pulse_width.format(channel=channel, pulse_width=pulse_width)) 

    @service
    def change_leading_edge(self, leading_edge, channel : int = 1):
        leading_edge = first_list_argument(leading_edge, self.rounding_places_pulse_edges)
        error_non_numerical(leading_edge, "change_leading_edge", "leading_edge", self.rounding_places_pulse_edges) #Checks if the argument is numeric.
        self._write(WRITE_COMMANDS.change_leading_edge.format(channel=channel, leading_edge=leading_edge)) #Value from 0 to 100%.

    @service
    def change_trailing_edge(self, trailing_edge, channel : int = 1):
        trailing_edge = first_list_argument(trailing_edge, self.rounding_places_pulse_edges)
        error_non_numerical(trailing_edge, "change_trailing_edge", "trailing_edge", self.rounding_places_pulse_edges) #Checks if the argument is numeric.
        self._write(WRITE_COMMANDS.change_trailing_edge.format(channel=channel, trailing_edge=trailing_edge)) #Value from 0 to 100%.

    @service
    def change_noise_bandwidth(self, noise_bandwidth, channel : int = 1):
        noise_bandwidth = first_list_argument(noise_bandwidth, self.rounding_places)
        error_non_positive(noise_bandwidth, "change_noise_bandwidth", "noise_bandwidth", self.rounding_places) #Checks if the argument is non positive.
        self._write(WRITE_COMMANDS.change_noise_bandwidth.format(channel=channel, noise_bandwidth=noise_bandwidth)) #Value from 0 to 100%.

    @service
    def change_bit_rate(self, bit_rate, channel : int = 1):
        bit_rate = first_list_argument(bit_rate, self.rounding_places)
        error_non_positive(bit_rate, "change_bit_rate", "noise_bandwidth", self.rounding_places) #Checks if the argument is non positive.
        self._write(WRITE_COMMANDS.change_bit_rate.format(channel=channel, bit_rate=bit_rate)) #Value from 0 to 100%.
    
    @service
    def change_edge_time(self, edge_time, channel : int = 1):
        edge_time = first_list_argument(edge_time, self.rounding_places_pulse_edges)
        error_non_numerical(edge_time, "change_edge_time", "offset", self.rounding_places_pulse_edges) #Checks if the argument is numeric.
        self._write(WRITE_COMMANDS.change_edge_time.format(channel=channel, edge_time=edge_time)) #Value from 0 to 100%.
    
    @service
    def change_configuration (self, args):
        change_specific_configuration(self, args, RESOURCE_DIR, FILE_NAME, INPUT_FORMAT, self.waveform_generator, CONTROLLER_NAME)
        
    @service
    def change_prbs_data(self, prbs_data : str, channel : int = 1):
        prbs_data = first_list_argument(prbs_data)        
        check_list_options(prbs_data, dir(ACCEPTED_PRBS_DATA_TYPES), "change_prbs_data", "function type")
        self._write(WRITE_COMMANDS.change_prbs_data.format(channel = channel,
                    prbs_data=getattr(ACCEPTED_PRBS_DATA_TYPES, prbs_data))) 
    
    @service
    def change_function_type(self, function_type : str, channel : int = 1):
        function_type = first_list_argument(function_type)        
        check_list_options(function_type, dir(ACCEPTED_FUNCTION_TYPES), "change_function_type", "function type")
        self._write(WRITE_COMMANDS.change_function_type.format(channel = channel,
                    function_type=getattr(ACCEPTED_FUNCTION_TYPES, function_type))) 
    """
    @service
    def change_function_type(self, function_type : str, channel : int = 1):
        function_type = first_list_argument(function_type)        
        check_list_options(function_type, dir(ACCEPTED_FUNCTION_TYPES), "change_function_type", "function type")
        a=function_type=getattr(ACCEPTED_FUNCTION_TYPES, function_type)
        visa_write("WRITE_COMMANDS", "change_function_type", channel, a, "here", self.waveform_generator)
        # self._write(WRITE_COMMANDS.change_function_type.format(channel = channel,
                    #function_type=getattr(ACCEPTED_FUNCTION_TYPES, function_type))) 
    """
    
    