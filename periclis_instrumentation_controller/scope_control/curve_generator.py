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

from periclis_instrumentation_controller.utils.file_parsing import *
from periclis_instrumentation_controller.utils.color_handling import *
from periclis_instrumentation_controller.scope_control.scope_reader import *
from periclis_instrumentation_controller.scope_control.controller_config import *
from periclis_instrumentation_controller.scope_control.save_data import save_data
from periclis_instrumentation_controller.scope_control.device_specific_commands import *

class curve_generator(save_data):        
    def curve_manager(self): #Manages other methods to generates the wave.
        print("Wait while the curve data is being saved... Expected maximum wait time: 10 seconds.")
        self.readscale()
        self.setting_acquisition(self.channel_std_trigger)
        (self.scaled_time, self.scaled_wave) = self.acquire_data(self.channel_std_trigger)
        self.acquire_new_channels()
        self.store_data()        

    def readscale(self):
        self.trigger_current_threshold = float(self._query(QUERY_COMMANDS.read_trigger_threshold.format()))
        self.wfm_record = int(self._query(READ_SCALE_CURVE_GENERATOR.read_scale_wfm_record.format()))  
        self.pre_trig_record = int(self._query(READ_SCALE_CURVE_GENERATOR.read_scale_pre_trig_record.format()))
        self.t_scale = float(self._query(READ_SCALE_CURVE_GENERATOR.read_scale_t.format()))
        self.t_sub = float(self._query(READ_SCALE_CURVE_GENERATOR.read_scale_t_sub.format())) # sub-sample trigger correction.
        self.v_scale = float(self._query(READ_SCALE_CURVE_GENERATOR.read_scale_v.format())) # volts / level.
        self.v_off = float(self._query(READ_SCALE_CURVE_GENERATOR.read_scale_v_off.format())) # reference voltage.
        self.v_pos = float(self._query(READ_SCALE_CURVE_GENERATOR.read_scale_v_pos.format())) # reference position (level).
    
    def setting_acquisition(self, channel):
        self.max_wave=0
        self._write(WRITE_ACQUISITION.change_acquisition_encdg.format(acquisition_encdg='SRIBINARY'))
        self._write(WRITE_ACQUISITION.change_acquisition_channel.format(acquisition_channel=('CH'+str(channel))))
        self._write(WRITE_ACQUISITION.change_acquisition_start.format(acquisition_start=1))
        self.acq_record = int(self._query(READ_SCALE_CURVE_GENERATOR.read_acquisition_horizontal.format()))
        self._write(WRITE_ACQUISITION.change_acquisition_stop.format(acquisition_stop = self.acq_record))
        self._write(WRITE_ACQUISITION.change_acquisition_byt_n.format(acquisition_byt_n=1))

    def acquire_data(self, channel): #Acquires data from scope.
        for count in range(int(self.acquisitions_retries)):
            try: 
                print(f"Will change to channel {channel}.")               
                self._write(WRITE_ACQUISITION.change_acquisition_channel.format(acquisition_channel=('CH'+str(channel))))
                print(f"Changed to channel {channel}.")
                self.acquire_curve()
                print(f"Data from channel {channel} acquired.")
                scaled_time = self.horizontal_wave()
                scaled_wave = self.vertical_wave()
                return (scaled_time, scaled_wave)
            except:
                print_yellow(f"Error in communication. Communication with the scope will be retried until {3-count} more times...")
                time.sleep(float(self.delay_acquisition_tentatives))
        if count == 3:
            raise Exception("Problem acquiring scope data! Check your connections")
         
    
    def acquire_curve(self): 
        self.bin_wave=self.scope_generator.query_binary_values('curve?', datatype='b', container=np.array, chunk_size = 1024**2)       
        self.max_wave=(max(self.bin_wave) - self.v_pos) * self.v_scale + self.v_off
        time.sleep(float(self.delay_acquisition)) #Delay to avoid too fast communication (seconds).  
    
    def horizontal_wave(self):
        self.total_time = self.t_scale * self.wfm_record
        self.t_start = (-self.pre_trig_record * self.t_scale) + self.t_sub
        self.t_stop = self.t_start + self.total_time
        return np.linspace(self.t_start, self.t_stop, num=self.wfm_record, endpoint=False)
        
    def vertical_wave(self):             
        self.unscaled_wave = np.array(self.bin_wave, dtype='double') # data type conversion 
        return ((self.unscaled_wave - self.v_pos) * self.v_scale + self.v_off)

    def acquire_new_channels(self):
        self.configurating_new_acquisitions()
        for channel in self.new_channels:
            print(f"Acquisition from channel (channel) will start...")
            _ , scaled_wave = self.acquire_data(channel)
            print(f"Storing data from channel {channel}.")
            setattr(self, f"scaled_wave{channel}", scaled_wave)
            self.list_scaled_wave_other_channels.append(f"scaled_wave{channel}")
            self.wave_minimums.append(min(scaled_wave))
            self.wave_maximums.append(max(scaled_wave))
        self.checking_wave_limits()

    def configurating_new_acquisitions(self):
        self.list_scaled_wave_other_channels = []
        self.wave_minimums = []
        self.wave_maximums = []
        if self.new_channels:
            print(f"Acquiring data from extra channels... Additional expected wait time: {len(self.new_channels)*10} seconds.")

    def checking_wave_limits(self):
        self.wave_minimums.append(min(self.scaled_wave))
        self.wave_maximums.append(max(self.scaled_wave))
        self.wave_lower_limit=min(self.wave_minimums)
        self.wave_upper_limit=max(self.wave_maximums)   

    def store_data(self): #Stores Scope data.
        save_data.store_data(self)

    


