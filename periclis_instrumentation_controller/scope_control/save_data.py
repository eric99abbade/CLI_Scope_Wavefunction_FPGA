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
import matplotlib.pyplot as plt # http://matplotlib.org/ - for plotting
import numpy as np # http://www.numpy.org
import datetime

from periclis_instrumentation_controller.utils.color_handling import *
from periclis_instrumentation_controller.utils.file_parsing import *
from periclis_instrumentation_controller.utils.data_conversion import *
from periclis_instrumentation_controller.scope_control.scope_reader import *
from periclis_instrumentation_controller.scope_control.device_specific_commands import *
from periclis_instrumentation_controller.scope_control.controller_config import *

class save_data():      
    def store_data(self): #Manages other methods to store data.
        print("Data is being saved on a figure and a csv file...")
        self.plot_parameters()
        self.date_seconds()
        self.save_csv()
        self.plot_configurations()  
        
    def plot_parameters(self):  
        channel_label = f"Voltage CH{self.channel_std_trigger} (V)"
        if self.trigger_use: #Case that the voltage measured is from an activated trigger.
            channel_label =  'Scope Triggered ' + channel_label 
        self.min_scale_time=min(self.scaled_time)
        self.max_scale_time=max(self.scaled_time)        
        self.fig, self.ax = plt.subplots()
        self.ax.plot(self.scaled_time, self.scaled_wave, label= channel_label, color='b') 
        self.plot_new_channels()    
    
    def plot_new_channels(self):                
        for voltage_new_channels in self.list_scaled_wave_other_channels:
            channel_label = f"Voltage CH{voltage_new_channels.replace("scaled_wave", "")} (V)"
            channel_color = channel_color_selector(int(voltage_new_channels.replace("scaled_wave", "")))
            self.ax.plot(self.scaled_time, getattr(self, voltage_new_channels), label=channel_label, color=channel_color) 

    def date_seconds(self): #Date until seconds.    
        self.hour=datetime.datetime.now().isoformat(timespec='hours') #Date with hour.
        self.minutes=datetime.datetime.now().minute
        self.seconds=datetime.datetime.now().second
        self.dt=str(self.hour)+'-'+str(self.minutes)+'-'+str(self.seconds) #Date with seconds, but without ":" character so that it can be used to save images.

    def save_csv(self):
        data=[]        
        self.defining_header_csv()
        data.append(self.header)
        for number in range(len(self.scaled_time)):
            list=[]
            list.append(round(self.scaled_time[number], int(self.rounding_places_time_acquisition)))
            list.append(round(self.scaled_wave[number], int(self.rounding_places_voltage_acquisition)))
            for voltage_new_channels in self.list_scaled_wave_other_channels:
                list.append(round(float((getattr(self, voltage_new_channels))[number]), int(self.rounding_places_voltage_acquisition)))
            data.append(list)
        write_file(data, Path(TRIGGER_THRESHOLD_DATA_DIR/f"Scope_Data{self.dt}{DATA_FORMAT}"), '.csv', self.header) #Saving the data with the date, so that old plots aren't overwritten. 

    def defining_header_csv(self):
        voltage_csv_title = 'voltage_ch'
        if self.trigger_use: #Case that the voltage measured is from an activated trigger.
            voltage_csv_title = 'triggered_' + voltage_csv_title
        self.header = ['time', voltage_csv_title+str(self.channel_std_trigger)]
        for channel in self.new_channels:
            self.header.append('voltage_ch'+str(channel))
        
    def plot_configurations(self): 
        self.trigger_identification()       
        plt.legend(loc="lower right")
        plt.title(self.fig_title) 
        plt.xlabel('Time (Seconds)') 
        plt.ylabel('Voltage (Volts)')   
        self.y_max_graph =  self.wave_upper_limit + 0.23*abs(self.wave_upper_limit-self.wave_lower_limit)   
        self.y_min_graph =  self.wave_lower_limit - 0.23*abs(self.wave_upper_limit-self.wave_lower_limit)  
        plt.ylim((self.y_min_graph), (self.y_max_graph))    
        plt.savefig(TRIGGER_THRESHOLD_PLOT_DIR/f"Scope_Plot{self.dt}{FIGURE_FORMAT}") #Saving the figure with the date, so that old plots aren't overwritten. 
        plt.show()

    def trigger_identification(self):
        if self.trigger_use:
            self.ax.hlines(y=self.trigger_current_threshold, xmin=self.min_scale_time, xmax=self.max_scale_time, label='Threshold Voltage(V)', color='r', linestyles='--')  #Minimal and Maximal (Volts) values of y-axis in plot.      
            self.fig_title = 'Voltage of trigger activation'
        else:
            self.fig_title = 'Current Voltage'
    