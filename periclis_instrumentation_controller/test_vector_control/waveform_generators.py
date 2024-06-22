# DAT/EMI - Electronics and Microelectronics Department
# Redistribution, modification or use of this software in source or binary
# forms is permitted as long as the files maintain this copyright. 

###############################################################################
# DAT/EMI and the Brazilian Center for Research in Energy and Materials (CNPEM)
# are not liable for any misuse of this material.
#
# @file waveform_generators.py
#
# @brief CLI for controlling OScilloscope, Wavegenerator and TestVector.
#
# @author Pedro Trindade 
# @author Eric Sonagli Abbade.
# @date 24/04/2024
###############################################################################
import numpy as np 
from periclis_instrumentation_controller.utils.data_conversion import calculate_slope

class wave_generator():
    # Generator in the waveform generator sense
    # not the design pattern generator sense
    def __init__(self, wavetype: str,
                    sampling_period: float,
                    number_samples: int,
                    vpp: float = None,
                    voltage_offset: float = None,
                    frequency: float = None,                     
                    threshold_voltage: float = None,
                    duty_cycle: float =None,
                    symmetry: float =None,
                    pulse_width: float =None,
                    lead_edge: float =None,
                    trail_edge: float =None
                    ): 
        self.wavetype = wavetype
        self.sampling_period = sampling_period
        self.number_samples = number_samples
        self.vpp = vpp
        self.voltage_offset = voltage_offset
        self.frequency = frequency        
        self.threshold_voltage = threshold_voltage
        self.symmetry = symmetry
        self.duty_cycle = duty_cycle
        self.pulse_width = pulse_width
        self.lead_edge = lead_edge
        self.trail_edge = trail_edge

    def get_waveform_output(self):        
        wavetype_name = "generate_" + self.wavetype
        try: # Get the method using getattr and call it
            self.wave_x_scale()
            generate_function = getattr(self, wavetype_name)
            generate_function()            
            return self.waveform_postprocessing()
        except AttributeError:
            raise Exception("Method '{}' does not exist.".format(wavetype_name))
        except Exception as error:
            raise Exception(f"Error Generating the waveform: {error}")

    def wave_x_scale(self):
        self.x = np.linspace(0, self.number_samples*self.sampling_period, self.number_samples)  
        self.period = 1 / self.frequency   
        self.t = self.x % self.period # Normalize time to the range [0, period).

    def waveform_postprocessing(self):
        self.waveform = self.waveform + self.voltage_offset 
        threshold_triggered = None        
        if self.threshold_voltage:
            threshold_triggered = self.waveform > self.threshold_voltage                     
        return self.waveform, self.x, threshold_triggered 
    
    def generate_sine(self):
        self.waveform = self.vpp*np.sin(2*np.pi*self.frequency*self.x) 

    def generate_square(self):
        self.waveform = np.zeros_like(self.x)
        for i, time in enumerate(self.t): # Generate the triangle wave
            if 0 <= time < self.period*self.duty_cycle:
                self.waveform[i] = self.vpp         
            else:
                self.waveform[i] = -self.vpp 
    
    def generate_ramp(self):
        try: 
            sign_slope = (0.5 - self.symmetry)/abs(0.5 - self.symmetry) #Determines the slope signal in the first cycle.
        except: #Case self.symmetry = 0.5, implies division by 0.
            sign_slope = 1 
        symmetry_coeficient = (1 - abs(1 - 2*self.symmetry)) #Determines the slope module in the first cycle.
        quarter_period_symmetry = (self.period / 4)*(symmetry_coeficient) #Duration of the first cycle.
        self.waveform = np.zeros_like(self.x)
        for i, time in enumerate(self.t): # Generate the triangle wave
            if 0 <= time < quarter_period_symmetry:
                x_initial = 0
                x_final = quarter_period_symmetry
                y_initial = 0
                y_final = self.vpp*sign_slope
                slope = calculate_slope(x_initial, x_final, y_initial, y_final)
                self.waveform[i] = slope * time
            elif quarter_period_symmetry <= time < (self.period - quarter_period_symmetry):
                x_initial = quarter_period_symmetry
                x_final = self.period - quarter_period_symmetry
                y_initial = self.vpp*(sign_slope)
                y_final = -self.vpp*(sign_slope)
                slope = calculate_slope(x_initial, x_final, y_initial, y_final)
                self.waveform[i] = y_initial + slope * (time - x_initial)
            else:
                x_initial = self.period - quarter_period_symmetry
                x_final = self.period
                y_initial = -self.vpp*(sign_slope)
                y_final = 0
                slope = calculate_slope(x_initial, x_final, y_initial, y_final)
                self.waveform[i] = y_initial + slope * (time - x_initial)               

    def generate_pulse(self):
        self.waveform = np.zeros_like(self.x)
        for i, time in enumerate(self.t): # Generate the triangle wave
            if 0 <= time < self.lead_edge:
                slope = calculate_slope(0, self.lead_edge, 0, self.vpp)
                self.waveform[i] = slope * time
            elif self.lead_edge <= time < (self.pulse_width - self.trail_edge):
                self.waveform[i] = self.vpp
            elif (self.pulse_width - self.trail_edge) <= time < self.pulse_width:
                x_initial = self.pulse_width - self.trail_edge
                x_final = self.pulse_width
                y_initial = self.vpp
                y_final = 0
                slope = calculate_slope(x_initial, x_final, y_initial, y_final)
                self.waveform[i] = y_initial + slope * (time - x_initial)
            else:
                self.waveform[i] = 0
    
    
    def generate_noise(self):
        self.waveform  = np.random.normal(loc=0, scale=self.vpp**0.5, size=len(self.x)) #Use waveform generator amplitude as gaussian variance.
    
    

