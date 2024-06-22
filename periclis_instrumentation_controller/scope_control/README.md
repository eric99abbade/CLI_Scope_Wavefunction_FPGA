## Oscilloscope Controller

## Brief Description

This folder manages communication with an oscilloscope, containing services for reading and writing its parameters.

## Connecting the Oscilloscope

This CLI allows the user to control oscilloscopes that are compatible with the **VISA** communication protocol.

Since this is a standard protocol for these devices on the market, many oscilloscopes are compatible with **VISA**.

In order to control these devices, you must connect them to the USB ports of your computer.

You can connect to every device that you want (even if it's more than one).

## Checking the Oscilloscope's Model

This CLI is tailored for controlling the **Tektronix MSO2024 Oscilloscope**.

If this is your intended device, no specific parameters or command syntax need to be specified, as they are already standardized.

Check if other models' command syntax matches those in the **device_specific_commands.py**.

To confirm the correct syntax for controlling an oscilloscope, search online about the **VISA** protocol or contact the manufacturer.

If the syntax differs from that in the **device_specific_commands.py files**, you'll need to edit these files accordingly.

## Connecting to an Oscilloscope

As explained in the README.md (of the PeriCLIs Instrumentation Controller), you can connect to a waveform generator with:

```sh
connect_resource 0 ScopeController
```

If the VISA ID's ResourceID differs from 0, substitute its value in the command above.

Or used a saved alias (such as "scope"), as explained when commenting about the conect_resource command, with:

```sh
connect_resource scope
```

## Oscilloscope's Services

**Services:** typing commands on the terminal, which work after establishing the connection with the WaveformController in the last section.

Type any of the commands (services) below after connecting with the controller (the **bold** values in parentheses are user-defined inputs):
- **read_trigger_state**
- **read_trigger_type**
- **read_trigger_channel**
- **read_trigger_coupling**
- **read_trigger_slope**
- **read_trigger_threshold**
- **read_trigger_holdoff**
- **read_scale_wfm_record**
- **read_scale_pre_trig_record**
- **read_scale_t**
- **read_scale_t_sub**
- **read_scale_v**
- **read_scale_v_off**
- **read_scale_v_pos**
- **change_trigger_type (<ins>trigger_type</ins>)**
- **change_trigger_channel (<ins>trigger_channel</ins>)**
- **change_trigger_coupling (<ins>trigger_coupling</ins>)**
- **change_trigger_slope (<ins>trigger_slope</ins>)**
- **change_trigger_threshold (<ins>trigger_threshold</ins>)**
- **change_trigger_holdoff (<ins>trigger_holdoff</ins>)**
- **change_scale_x (<ins>scale_x</ins>)**
- **change_scale_y (<ins>scale_y</ins>)**
- **autoscale**

- **read_default_configurations**
- **read_configurations**
- **read_channel_state**
- **read_state_trigger**
- **read_instrument_timeout**
- **read_probe_gain**
- **read_x_scale**
- **read_y_scale**
- **read_reference_level**
- **read_voltage_threshold_trigger**
- **read_holdoff_trigger**
- **read_type_trigger**
- **read_channel_trigger**
- **read_coupling_trigger**
- **read_slope_trigger**
- **monitore_dc_voltage**
- **autoscale**
- **button_single**
- **press_run_stop**
- **default_configurations**
- **change_channel_on**
- **change_channel_off**
- **change_configuration**, args: configuration_name, configuration_value
- **change_instrument_timeout**, args: Timeout to be waited until communication finishes (s).
- **change_probe_gain**, args: Gain of the probe that multiplies the value read.
- **change_x_scale**, args: Trigger horizontal scale (value of the scope full screen x-axis in seconds)
- **change_y_scale**, args: Trigger vertical scale (value of the scope full screen y-axis in Volts)
- **change_reference_level**, args: Voltage level position (reference value in Volts "0 V" according to full screen y-axis scale)
- **change_voltage_threshold_trigger**, args: Voltage threshold(V) (Scale must allow the threshold! Only multiples of 40 mV in some Scopes)
- **change_holdoff_trigger**, args: Holdoff Time(s)
- **change_type_trigger**, args: Type, examples: [bus, edge, logic, pulse, video]
- **change_channel_trigger**, args: Source (channel), examples: [ch1, ch2, ch3, ch4]
- **change_coupling_trigger**, args: Coupling, examples: [dc, hf, lf, noise]
- **change_slope_trigger**, args: Slope, examples: [fall, rise]
- **use_trigger_mode**, args: Configurations (0:scope_config.csv / 1:scope), Scale (0:scope_config.csv / 1:scope / 2:autoscale). Default:(0, 0)

<br></br> 

You can view the list above in the CLI after typing the following (if connected to the controller):

```sh
services_list
```

You can type the following service (or any from the list above) command in the terminal after connecting to the controller:

```sh
change_voltage_threshold_trigger 4.0
```

The service command above adjusts the oscilloscope's trigger threshold to the "Voltage threshold" argument (in volts), so in this case it will be 4.0 V. <br></br>

Reading commands, which don't require input values, work like this:

```sh
read_voltage_threshold_trigger
```

It identifies the threshold and prints its value in volts:

```sh
4.000
```

<br></br>
Following this logic, all list service commands can be utilized. Below is a description of each command's functionality:
- **read_state_trigger** - *prints: trigger state.*
- **read_type_trigger**  *prints: trigger type (see **Oscilloscope trigger types** below).*
- **read_channel_trigger** *prints: trigger channel (see **Oscilloscope trigger channels** below)*. 
- **read_coupling_trigger** *prints: trigger coupling(see **Oscilloscope trigger coupling** below).* 
- **read_slope_trigger** *prints: trigger slope (see **Oscilloscope trigger slopes** below)*. 
- **read_voltage_threshold_trigger** *prints: trigger threshold (volts).*
- **read_holdoff_trigger** *prints: trigger holdoff  (seconds).*
- **read_scale_wfm_record** *prints: the number of points*
- **change_type_trigger (<ins>Type</ins>)** *changes trigger type to (<ins>Type</ins>). See **Oscilloscope trigger types** below.*
- **change_channel_trigger (<ins>channel</ins>)** 
*changes trigger channel to (<ins>channel</ins>). See **Oscilloscope trigger channel** below.*
- **change_coupling_trigger (<ins>Coupling</ins>)** *changes trigger coupling to (<ins>Coupling</ins>). See **Oscilloscope trigger coupling** below.*
- **change_slope_trigger (<ins>Slope</ins>)**
*changes trigger_slope to (<ins>Slope</ins>). See **Oscilloscope trigger slope** below.*
- **change_voltage_threshold_trigger (<ins>Voltage threshold</ins>)** *changes trigger threshold voltage (volts) to(<ins>Voltage threshold</ins>)*
- **change_holdoff_trigger (<ins>Holdoff Time</ins>)**
*changes trigger holdoff time (seconds) to (<ins>Holdoff Time</ins>)*
- **change_scale_x (<ins>horizontal scale</ins>)** *changing time scale, 1 scope's square to **<ins>(horizontal scale)</ins>** in seconds."*
- **change_scale_y (<ins>vertical scale</ins>)**  *changing voltage scale, 1 scope's square to **<ins>(vertical scale)</ins>** in Volts."*
- **autoscale**: *realizes the autoset of the oscilloscope.*
<br> </br> <br> </br>  

The data below corresponds to oscilloscope trigger options (left) and their respective writing commands (right). 

In order to write commands, you have to type them as they are written on the right side of the equation, after the equal (=) simple. 

For instance, to change the trigger channel to channel 2, with the command mentioned before, type the following line using CH2:

```sh
change_trigger_channel CH2
```
In order to use the read commands, you can see the options that you might expect on the lists below. 

The parameters read are going to appear in a similar format to what is shown below. 

**Oscilloscope trigger types:**<br> 
- edge type = edge
- logic type = logic
- pulse type = pulse 
- bus type = bus
- video type = video<br> </br>
    
**Oscilloscope trigger channels:**
- Channel 1 = CH1
- Channel 2 = CH2
- Channel 3 = CH3
- Channel 4 = CH4<br> </br>

**Oscilloscope trigger coupling:**
- DC VOltage = dc
- High frequency reject = hf 
- Low frequency reject = lf 
- Noise reject = noise <br> </br>

**Oscilloscope trigger slope:**<br> 
- rising border = rise
- falling border = fall
