# Waveform Controller

## Brief Description

This folder manages communication with a voltage waveform generator. It includes services for reading and writing parameters like:

- Amplitude,
- Frequency,
- Offset,
- Phase,
- Function type (sinusoid, square, triangle, ramp, pulse, noise, random bits, DC),
- Some general configuration settings.

## Connecting the Waveform Controller

This CLI allows the user to control waveform generators that are compatible with the **VISA** communication protocol.

Since this is a standard protocol for these devices on the market, many waveform generators are compatible with **VISA**.

In order to control these devices, you must connect them to the USB ports of your computer.

You can connect to every device that you want (even if it's more than one).

## Checking the Waveform Generator's Model

This CLI is tailored for controlling the **Keysight 33500B Waveform Generator**.

If this is your intended device, no specific parameters or command syntax need to be specified, as they are already standardized.

For other device models, verify if their command syntax matches those in the **device_specific_commands.py** file.

To confirm the correct syntax for controlling a waveform generator, search online about the **VISA** protocol or contact the manufacturer.

If the syntax differs from that in the **device_specific_commands.py files**, you'll need to edit these files accordingly.

## Connecting to a Waveform Generator

As explained in the README.md (of the PeriCLIs Instrumentation Controller), you can connect to a waveform generator with:

```sh
connect_resource 0 WaveformController
```

If the VISA ID's ResourceID differs from 0, substitute its value in the command above.

## WaveformController's Services

**Services:** typing commands on the terminal, which work after establishing the connection with the WaveformController in the last section.

Type any of the commands (services) below after connecting with the controller (the <ins>underline</ins> values in parentheses are user-defined inputs):

- **dummy**
- **query_info**
- **read_all**
- **read_voltage**
- **read_frequency**
- **read_offset**
- **read_phase**
- **read_function_type**
- **change_voltage (<ins>voltage</ins>)**
- **change_frequency_hz (<ins>frequency</ins>)**
- **change_offset (<ins>offset</ins>)**
- **change_phase (<ins>phase</ins>)**
- **change_function_type (<ins>function_type</ins>)**<br></br>

You can view the list above in the CLI after typing the following (if connected to the controller):

```sh
list_services
```

You can type the following service (or any from the list above) command in the terminal after connecting to the controller:

```sh
change_voltage 1.5
```

The service command above adjusts the waveform generator's amplitude to (voltage) volts, so in this case it will be 1.5 V. <br></br>

Reading commands, which don't require input values (<ins>underline</ins> values in parentheses), work like this:

```sh
read_voltage
```

It identifies the amplitude and prints its value in volts:

```sh
1.500
```

<br></br>
Following this logic, all list service commands can be utilized. Below is a description of each command's functionality:

- **dummy** - _prints: Just a testing service_.
- **query_info** - _prints: the concatenation of the results of_: '*IDN?', '*OPT?', and '_OPC?' _(search these **VISA** commands for more info)\*.
- **read_all** - _prints: wave format (see **Waveform generator function types** below), frequency (Hz), amplitude (Volts), and offset (Volts)._
- **read_voltage** - _prints: amplitude (Volts)._
- **read_frequency** - _prints frequency (Hz)._
- **read_offset** - _prints: offset (Volts)._
- **read_phase** - _prints: phase (Celsius Degrees)._
- **read_function_type** - _prints: the functions type (see **Waveform generator function types** below)._
- **change_voltage <ins>(voltage)**-</ins>
  _change amplitudes to **<ins>(voltage)</ins>** in volts._
- **change_frequency_hz <ins>(frequency)** </ins> - _change frequency to **<ins>(frequency)</ins>** in Hertz._
- **change_offset <ins>(offset)** -</ins> _change offset to **<ins>(offset)</ins>** in volts_.
- **change_phase <ins>(phase)** -</ins> _change phase to **<ins>(phase)</ins>** in Celsius Degrees._
- **change_function_type <ins>(function_type)** -</ins> _change function type to **<ins>(function_type)</ins>** (see **Waveform generator function types** below)._

**Waveform generator function types:**<br>
sine='SINusoid', square='SQUare', triangle='TRIangle', ramp='RAMP', pulse='PULSe', noise='NOIS', random_bits='PRBS', and step='DC'.
