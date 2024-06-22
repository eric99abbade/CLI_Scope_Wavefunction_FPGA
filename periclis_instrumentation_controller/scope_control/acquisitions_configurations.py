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

import time
from periclis_instrumentation_controller.utils.color_handling import *
from periclis_instrumentation_controller.utils.data_conversion import *
from periclis_instrumentation_controller.scope_control.curve_generator import curve_generator
from periclis_instrumentation_controller.scope_control.device_specific_commands import WRITE_COMMANDS, QUERY_COMMANDS, ACCEPTED_TRIGGER_TYPES, ACCEPTED_CHANNELS, ACCEPTED_TRIGGER_COUPLING, ACCEPTED_TRIGGER_SLOPE

class acquisitions_configurations(curve_generator):
    def __init__(self, trigger, configurated, scale, channel):  
        print("Wait while the scope is being configurated... Expected maximum wait time: 10 seconds.")  
        self.possible_new_channels = [self.add_channel_trigger_plot_1, self.add_channel_trigger_plot_2, self.add_channel_trigger_plot_3]   
        self.initial_configuirations(configurated)
        self.configuration_manager(trigger, configurated, scale, channel)

    def initial_configuirations(self, configurated): 
        self._write(WRITE_COMMANDS.change_channel_on.format(channel=int(self.channel_std_trigger))) 
        time.sleep(float(self.delay_general_commands)) #Delay for general commands in seconds.
        if configurated==0: #If using standard configurations, the probe gain will assume the pre-defined value.
            self._write(WRITE_COMMANDS.change_probe_gain.format(channel=int(self.channel_std_trigger), gain=1/(float(self.probe_gain)))) #Probe must be changed before scale, because it changes scale (but changing scale, doesn't change the probe gain).
            time.sleep(float(self.delay_general_commands)) #Delay for general commands in seconds.
        position = float(self.reference_level)/float(self._query(QUERY_COMMANDS.read_scale_y.format(channel=int(self.channel_std_trigger)))) #Y scale value of a channel square in Volts.
        self._write(WRITE_COMMANDS.change_reference_level.format(channel=int(self.channel_std_trigger), position=position))
        time.sleep(float(self.delay_general_commands)) #Delay for general commands in seconds.
        
    def configuration_manager(self, trigger, configurated, scale, channel):
        if trigger: #Case for using trigger.
            self.trigger_manager(configurated, scale, channel)
        else: #Case for capturing current voltage.
            self.add_new_channels(self.possible_new_channels, configurated)
            curve_generator.curve_manager(self)

    def trigger_manager(self, configurated, scale, channel):
        self.scale_selector(configurated, scale)   
        self.configurate_selector(configurated)        
        self.add_new_channels(self.possible_new_channels, configurated)
        self.trigger_checker(self.activate_trigger_mode())      

    def scale_selector(self, configurated, scale): 
        if scale == 1:   
            print("Using Scale already defined on Scope!")  
        elif scale == 2:
            self.autoscale_trigger(configurated)      
        else:
            print("Using Scale defined on scope_config.csv file!")
            self.scale() 
            time.sleep(float(self.delay_scale)) #Time needed until scale is done in seconds.

    def autoscale_trigger(self, configurated):
        if configurated == 1: #For using the trigger configurations from before the Autoscale, it's necessary to save Threshold and Holdoff parameters, otherwise they will be reset. 
            print("Scope Autoscale usually resets Threshold and Holdoff. However, these parameters will be saved to be reused after the Autoscale.")
            (autoscale_threshold, autoscale_holdoff) = self.read_trigger_autoscale()
            self.autoscale()
            self.write_trigger_autoscale(autoscale_threshold, autoscale_holdoff)
        else:
            self.autoscale()
        print("Wait some seconds until autoscale is finished!")
        time.sleep(float(self.delay_autoscale)) #Time needed until autoscale is done in seconds. 
    
    def read_trigger_autoscale(self):
        autoscale_threshold = self._query(QUERY_COMMANDS.read_trigger_threshold.format())  
        autoscale_holdoff = self._query(QUERY_COMMANDS.read_trigger_holdoff.format())  
        return (autoscale_threshold, autoscale_holdoff)  
    
    def autoscale(self):
        self._write(WRITE_COMMANDS.autoscale)
    
    def write_trigger_autoscale(self, autoscale_threshold, autoscale_holdoff):
        self._write(WRITE_COMMANDS.change_trigger_threshold.format(trigger_threshold=float(autoscale_threshold))) #Standard value for trigger threshold.
        self._write(WRITE_COMMANDS.change_trigger_holdoff.format(trigger_holdoff=float(autoscale_holdoff))) #Standard value for trigger holdoff.
    
    def scale(self):   
        self._write(WRITE_COMMANDS.change_scale_x.format(scale_x=float(self.time_scale)/(float(self.squares_x_axis))))    
        self._write(WRITE_COMMANDS.change_scale_y.format(channel=int(self.channel_std_trigger), scale_y=float(self.voltage_scale)/(float(self.squares_y_axis))))  
        
    def configurate_selector(self, configurated):
        if configurated == 1:
            print("Using Configurations already defined on Scope!")  
        else:
            print("Using Configurations defined on scope_config.csv file!")
            self.configurating_trigger_parameters() 

    def configurating_trigger_parameters(self):           
        self._write(WRITE_COMMANDS.change_trigger_type.format(trigger_type=getattr(ACCEPTED_TRIGGER_TYPES, self.type_std_trigger))) #Standard value for trigger format.     
        self._write(WRITE_COMMANDS.change_trigger_channel.format(trigger_channel=int(self.channel_std_trigger))) #Standard value for trigger channel. 
        self._write(WRITE_COMMANDS.change_trigger_coupling.format(trigger_coupling=getattr(ACCEPTED_TRIGGER_COUPLING, self.coupling_std_trigger))) #Standard value for trigger coupling. 
        self._write(WRITE_COMMANDS.change_trigger_slope.format(trigger_slope=getattr(ACCEPTED_TRIGGER_SLOPE, self.slope_std_trigger))) #Standard value for trigger slope.
        self._write(WRITE_COMMANDS.change_trigger_threshold.format(trigger_threshold=float(self.threshold_std_trigger))) #Standard value for trigger threshold.
        self._write(WRITE_COMMANDS.change_trigger_holdoff.format(trigger_holdoff=float(self.holdoff_std_trigger))) #Standard value for trigger holdoff.
        
    def add_new_channels(self, possible_new_channels, configurated): 
        self.new_channels = []
        for channel in possible_new_channels:
            if int(channel): #If channel = 0, it will be considered as if there are no extra channels.
                if channel <= self.number_channels:
                    try:
                        channel = int(remove_channel_prefix(channel))              
                        self.new_channels.append(channel)
                    except:                
                        print_yellow("Invalid Extra Channel! Check self.add_channel_trigger_plot_1 on scope_config.csv!")
                else:
                    print_yellow(f"Invalid channel CH{channel}! Scope has only {self.number_channels} channels! Check scope_config.csv file!")
        self.configurating_new_channel(configurated)
    
    def configurating_new_channel(self, configurated): 
        if self.new_channels:
            position = float(self._query(QUERY_COMMANDS.read_reference_level.format(channel=int(self.channel_std_trigger)))) 
            y_square = float(self._query(QUERY_COMMANDS.read_scale_y.format(channel=int(self.channel_std_trigger))))       
            time.sleep(float(self.delay_general_commands)) #Delay for general commands in seconds.
        for channel in self.new_channels:
            self._write(WRITE_COMMANDS.change_channel_on.format(channel=int(channel)))
            if configurated==0: #If using standard configurations, the probe gain will assume the pre-defined value.
                self._write(WRITE_COMMANDS.change_probe_gain.format(channel=int(channel), gain=1/(float(self.probe_gain)))) #Probe must be changed before scale, because it changes scale (but changing scale, doesn't change the probe gain).
            self._write(WRITE_COMMANDS.change_scale_y.format(channel=channel, scale_y=y_square)) #Y scale value of the standard channel square in Volts.
            self._write(WRITE_COMMANDS.change_reference_level.format(channel=int(channel), position=position)) #Position of the standard channel in Volts. 
            time.sleep(float(self.delay_general_commands)) #Delay for general commands in seconds.
        
    def activate_trigger_mode(self):
        counter = 0
        while(self._query(QUERY_COMMANDS.read_trigger_state.format())[:-1]!='READY'):             
            self._write(WRITE_COMMANDS.single) #This command equals to pressing the single button.
            time.sleep(float(self.delay_single_pressing)) #Delay that the Single button will be pressed (seconds).
            counter=counter+1
            if counter==int(self.tentatives_single_activating):                 
                return self.instant_image_check()
        return "Trigger_Activated"

    def instant_image_check(self):        
        if (self._query(QUERY_COMMANDS.read_trigger_state.format())[:-1]=='SAV') or (self._query(QUERY_COMMANDS.read_trigger_state.format())[:-1]=='TRIG'): #Case that trigger is already activated.
            print_yellow("Warning! Trigger is already activated at the start of the application!")
            return "Image_Already_Saved"
        else:
            print_red("Error! Failed activating triggering mode with the use of Single! Check your scope configurations!")
            return "Error_Activating_Trigger"
        
    def trigger_checker(self, trigger_config):
        while (self._query(QUERY_COMMANDS.read_trigger_state.format())[:-1]=='READY'):            
            print(get_blue("Current trigger state is:"), get_green(self._query(QUERY_COMMANDS.read_trigger_state.format())[:-1]))
            time.sleep(float(self.delay_check_wave)) #Delay (seconds) between checks of trigger state.
        if trigger_config != 'Error_Activating_Trigger':
            self.trigger_use = True #Variable for plot with threshold.
            curve_generator.curve_manager(self)
