from periclis_instrumentation_controller.test_vector_control.virtual_device import Waveform
import numpy as np
from matplotlib.axes import Axes

def plot_waveform(waveform : Waveform, ax : Axes,
                  threshold_voltage: float=0,
                  voltage_offset: float = 0,
                  fixed_point : bool=False,
                  symmetric_threshold : bool=False):
        
    if not waveform.data_valid:
            raise Exception("Data not valid to plot")

    output_samples = waveform.fixed_point_samples if fixed_point \
                                     else waveform.output_samples
    
    drawstyle = 'steps-post' if fixed_point else 'default'

    x_axis = waveform.time_range
    
    ax.plot(x_axis, output_samples, drawstyle=drawstyle)

    if waveform.where_triggered is not None:
        # Generate the plot for passing threshold
        upper_threshold = voltage_offset + threshold_voltage
        threshold_passed = np.where(output_samples < upper_threshold, 
                                    upper_threshold, output_samples)

        ax.plot(x_axis, threshold_passed.tolist(),
                color='orangered', drawstyle=drawstyle)
        
        if symmetric_threshold == True: 
            # Generate the plot for passing threshold
            lower_threshold = voltage_offset - threshold_voltage
            threshold_passed = np.where(output_samples > lower_threshold,
                                        lower_threshold, output_samples)

            ax.plot(x_axis, threshold_passed.tolist(),
                    color='orangered', drawstyle=drawstyle)
    
def plot_threshold_lines(ax : Axes,
                         threshold_voltage: float,
                         voltage_offset: float = 0,
                         symmetric_threshold: bool = False):
        
        # plots the threshold horizontal line
        ax.axhline(y=threshold_voltage + voltage_offset, color='purple',
                        linestyle='--', linewidth=2.5)
        
        if symmetric_threshold == True:
             # plots a second symmetric threshold horizontal line
            ax.axhline(y=voltage_offset - threshold_voltage, color='purple',
                            linestyle='--', linewidth=2.5)
        