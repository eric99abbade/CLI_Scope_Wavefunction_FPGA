# DAT/EMI - Electronics and Microelectronics Department
# Redistribution, modification or use of this software in source or binary
# forms is permitted as long as the files maintain this copyright. 

###############################################################################
# DAT/EMI and the Brazilian Center for Research in Energy and Materials (CNPEM)
# are not liable for any misuse of this material.
#
# @file test_vector_resource_handler.py
#
# @brief CLI for controlling OScilloscope, Wavegenerator and TestVector.
#
# @author Pedro Trindade 
# @author Eric Sonagli Abbade.
# @date 24/04/2024
###############################################################################
from periclis_instrumentation_controller.utils.decorators import service_add  
from periclis_instrumentation_controller.test_vector_control.virtual_device import VirtualDevice
from periclis_instrumentation_controller.test_vector_control.plot_functions import plot_waveform, plot_threshold_lines
from periclis_instrumentation_controller.utils.color_handling import *

from periclis_instrumentation_controller.test_vector_control.services_metainfo import SERVICES_METAINFO
from periclis_instrumentation_controller.test_vector_control.controller_config import *
from periclis_instrumentation_controller.utils.file_parsing import *
from periclis_instrumentation_controller.utils.errors_handling import first_list_argument, error_file

import matplotlib.pyplot as plt 
import random
import logging



# A decorator facilitating listing services boilerplate
service = service_add(controller_name=CONTROLLER_NAME, 
                      services_metainfo=SERVICES_METAINFO)

class TestVectorResourceHandler:
    def __init__(self, resource : str) -> None:
        self.resource_file_name = resource
        self.resource= VirtualDevice(resource)
        self.complete_input_data_path = DEFAULT_RESOURCE_DIR / EXTRA_RESOURCE_DIR

    last_file_saved : str = None 
    
    @service
    def new_resource(self, args):        
        try:
            name=str(first_list_argument(args))
            (name, file_format) = split_file_format(name)
        except:
            raise Exception("Must inform the name of the file (including the folder path and the .json or the desired format at end) after command!")                         
        if checking_file_on_directory(self.complete_input_data_path, name, file_format):
            raise Exception("There is already a resource with this name!")
        create_file(self.complete_input_data_path, name, file_format)
    
    @service
    def delete_resource(self, args):
        try:
            name=str(first_list_argument(args))
            (name, file_format) = split_file_format(name)
        except:
            raise Exception("Must inform the name of the file (including the folder path and the .json or the desired format at end) after command!")  
        if name==STANDARD_INPUT_FILE:
            raise Exception("This is the standard file that cannot be removed!")         
        delete_file(self.complete_input_data_path / Path(name+file_format))

    @service
    def change_resource_config (self, args):   
        if self.resource_file_name==(str(EXTRA_RESOURCE_DIR + '/' + STANDARD_INPUT_FILE + DEFAULT_INPUT_FORMAT)):
            raise Exception("This is the standard file that cannot be edited!") 
        (name, file_format) = split_file_format(self.resource_file_name) 
        change_file (self, args, DEFAULT_RESOURCE_DIR, name, file_format, CONTROLLER_NAME)   
        try:
            self.resource = VirtualDevice(self.resource_file_name)
        except Exception as error:
            print_red(f"Error while updating resource file : {error}")     
        
    @service
    def copy_resource (self, args):
        try:
            name = str(first_list_argument(args))
            (name, file_format) = split_file_format(name)
            (resource_file_name, resource_format) = split_file_format(self.resource_file_name)
        except:
            raise Exception("Must inform the name of the file (including the folder path and the .json or the desired format at end) after command!")                         
        if name == str(STANDARD_INPUT_FILE):
            raise Exception("This is the standard file that cannot be edited!") 
        if not checking_file_on_directory(DEFAULT_RESOURCE_DIR, name, file_format):
            raise Exception("There is not any resource with this name!")    
        data_read = read_file((DEFAULT_RESOURCE_DIR / Path(resource_file_name+resource_format)), resource_format)
        update_file(data_read, (DEFAULT_RESOURCE_DIR / Path(name+file_format)), file_format, CONTROLLER_NAME)
        print_green("Returned to default configurations!")

    @service
    def read_resource_configs(self):
        print_green("\n> Resource Configuration Values:\n")
        for item in self.resource.config_attrs.keys():
            print(get_blue(f'\t- {item},')
                  + get_green(f' value: {self.resource.config_attrs[item]}'))
        print("\n")

    @service
    def generate_testvector (self):
        try: 
            self.resource.generate_test_vector()
            print_green("TestVector Generation was Successful")
        except Exception as error:
            print_red(f"TestVector Generation was not Successful: {error}")
        
    @service
    def plot_testvector (self):
        try:
            fig, (ax1, ax2)= plt.subplots(2)

            ax1.set_title("Generated Waveform")
            ax1.set_xlabel("Time (s)")
            ax1.set_ylabel("Voltage (V)")
            plot_waveform(self.resource.output_waveform, ax1, 
                          self.resource.threshold_voltage,
                          voltage_offset=self.resource.voltage_offset,
                          symmetric_threshold=self.resource.symmetric_threshold)
            
            plot_threshold_lines(ax1, self.resource.threshold_voltage,
                                 self.resource.voltage_offset, 
                                 self.resource.symmetric_threshold)
            

            ax2.set_title("Fixed-Point Truncated Waveform")
            ax2.set_xlabel("Time (s)")
            ax2.set_ylabel("Voltage (V)")
            # Plot fixed point representation of waveform
            plot_waveform(self.resource.output_waveform, ax2,
                          self.resource.threshold_voltage,
                          voltage_offset=self.resource.voltage_offset,
                          fixed_point=True,
                          symmetric_threshold=self.resource.symmetric_threshold)

            plot_threshold_lines(ax2, self.resource.threshold_voltage,
                                 self.resource.voltage_offset, 
                                 self.resource.symmetric_threshold)

            fig.tight_layout(pad=2.0)
            fig.show()
        except Exception as error:
            print_red(f"Plotting data was not successful: {error}")
    
    @service
    def save_testvector(self, args=None):
        args = first_list_argument(args) 
        #error_file(args, "json", "change_function_type", "function type")
        try:
            if self.resource.output_waveform.data_valid == False:
                logging.warning("Data saved is not up to date")

            # Generates random name if one is not given
            out_file_name = TEST_VECTOR_OUTPUT_DEFAULT_NAME.format(id=random.randint(1, 1000)) \
                            + '.json'

            if args is not None:
                out_file_name = args

            self.last_file_saved = out_file_name
            out_file_path = TEST_VECTOR_OUTPUT_PATH / out_file_name

            if not check_if_file_exists(out_file_path): 
                
                waveform = self.resource.output_waveform
                waveform_dict = {"fixed_point_samples": list(waveform.fixed_point_samples()),
                                    "binary_representation_samples": waveform.raw_binary_samples,
                                    "trigger": waveform.where_triggered.tolist()}
                writting_success = False

                if out_file_name.endswith(".json"):
                    write_file(waveform_dict, str(out_file_path), '.json')
                    writting_success = True
                ## outputs basic VHDL Textvector
                elif out_file_name.endswith(".txt"):
                    ## Formatting the dict to facilitate processing with VHDL
                    waveform_dict.pop("fixed_point_samples")
                    ## passed bool to 0 and 1
                    waveform_dict["trigger"] = [int(value) for value in waveform_dict["trigger"]]
                    
                    write_txt_from_dict(waveform_dict, out_file_path)
                    writting_success = True
                else:
                    raise Exception("File Format Not Supported")
                
                if writting_success: print_green(f"Successfully wrote File {out_file_name} !")
                
            else: 
                raise Exception("File already Exists, please try again")
             
        except Exception as error:
            print_red(f"Error happened while saving the plot: {error}")
    
    @service
    def delete_testvector(self, args=None):
        args = first_list_argument(args)
        error_file(args, "json", "change_function_type", "function type")
        try: 
            if args is None:
                out_file_name = self.last_file_saved
            elif not isinstance(args, str) and len(args) > 1:
                raise Exception(f"Too Many Args...")
            else:
                out_file_name = args

            out_file_path = TEST_VECTOR_OUTPUT_PATH / out_file_name

            if not check_if_file_exists(out_file_path):
                raise Exception(f"File does not exist to be deleted")

            delete_file(out_file_path)

        except Exception as error:
            print_red(f"Error happened while deleting the testvector: {error}")
    
    @service
    def list_testvectors (self):
        pass

 

    
        
    