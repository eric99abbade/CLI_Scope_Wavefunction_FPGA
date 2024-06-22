# DAT/EMI - Electronics and Microelectronics Department
# Redistribution, modification or use of this software in source or binary
# forms is permitted as long as the files maintain this copyright. 

###############################################################################
# DAT/EMI and the Brazilian Center for Research in Energy and Materials (CNPEM)
# are not liable for any misuse of this material.
#
# @file virtual_device.py
#
# @brief CLI for controlling OScilloscope, Wavegenerator and TestVector.
#
# @author Pedro Trindade 
# @author Eric Sonagli Abbade.
# @date 24/04/2024
###############################################################################

from periclis_instrumentation_controller.test_vector_control.resource_file_parse import resource_file_parse
from periclis_instrumentation_controller.test_vector_control.waveform_generators import wave_generator

from periclis_instrumentation_controller.utils.data_conversion import convert_fixed

import logging
# Handles fixed point data 
from fxpmath import Fxp

class Waveform:
    output_samples : list [float] = []
    fixed_point_samples : Fxp = []
    raw_binary_samples : list[str] = []
    # Time Range of the samples
    time_range : list[float] = []
    # Optionally you can use this to add
    # new information about the samples
    optional_metadata : dict = {}
    # Use this attr to check if the data is
    # consumer-ready instead of handling
    # many exceptions.
    data_valid : bool = False

    # For data with threshold 
    where_triggered : list[bool] = None

class VirtualDevice:
    config_attrs : dict = None
    output_waveform : Waveform = Waveform() 
    
    def __init__(self, resource_name : str=None) -> None:
        if resource_name: 
            self.config_attrs = resource_file_parse(resource_name)
            self.add_virtual_file_attrs(self.config_attrs)
            
    # This adds the file defined variables as attributes to this class
    # @TODO think better if this is a good ideia
    def add_virtual_file_attrs(self, attrs: dict[str, str | float | int]):
        for attr_name in attrs.keys(): 
            attr_value = attrs[attr_name]
            setattr(self, attr_name, attr_value)
    
    def generate_waveform(self) -> dict: 
        try:
            threshold_voltage = self.threshold_voltage if hasattr(self, 'threshold_voltage') else None
            
            # Constructs the wave form generator with the options in the config json
            wave_gen = wave_generator(
                wavetype=getattr(self, 'wave_type', None),
                sampling_period=getattr(self, 'sampling_period', None),
                number_samples=getattr(self, 'number_samples', None),
                vpp=getattr(self, 'vpp_voltage', None),
                voltage_offset=getattr(self, 'voltage_offset', None),
                frequency=getattr(self, 'frequency', None),
                threshold_voltage=threshold_voltage,
                symmetry=getattr(self, 'symmetry', None),
                duty_cycle=getattr(self, 'duty_cycle', None),
                pulse_width=getattr(self, 'pulse_width', None),
                lead_edge=getattr(self, 'lead_edge', None),
                trail_edge=getattr(self, 'trail_edge', None)
            )
            output_samples, x, where_triggered = wave_gen.get_waveform_output()
            
            self.output_waveform.output_samples = output_samples
            self.output_waveform.time_range = x
            self.output_waveform.where_triggered = where_triggered
            self.output_waveform.data_valid = True
                  

            self.output_waveform.output_samples = output_samples
            self.output_waveform.time_range = x
            self.output_waveform.where_triggered = where_triggered
            self.output_waveform.data_valid = True

            
        except Exception as error: 
            logging.exception("Failed to generate Waveform: {error}")
            self.output_waveform.data_valid = False
            raise error

    def pass_waveform_to_fixed(self, waveform : Waveform):
        try:
            if waveform.data_valid == True:
                waveform.fixed_point_samples = convert_fixed(list(waveform.output_samples),
                                                             size=self.bits_resolution,
                                                             fraction_size=self.fractional_repr,
                                                             signed=self.signed) 

                waveform.raw_binary_samples = waveform.fixed_point_samples.bin()

            else:
                raise Exception("Waveform not valid") 
        except Exception as error:
            logging.exception("Something Went wrong in "+ 
                              f"passing the waveform to fixed point: {error}")           
            raise error

    def generate_test_vector(self):
        try: 
            self.generate_waveform()
            self.pass_waveform_to_fixed(self.output_waveform) 
        except Exception as error:
            logging.exception(f"Test Vector Generation Error:{error}")
            raise error
   