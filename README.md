# Programmable-Environment for Reliable Instrumentation CLI System (PeriCLIs)

## Brief Description

Command Line Interface (CLI) for controlling and reading electrical signals, accessible via the OS terminal. It reads data from oscilloscopes (continuously or post-trigger), adjusts waveform generator's voltages and also controls their parameters. This is done using the **VISA** communication protocol, which connects to compatible devices via their **VISA ID**. The CLI also generates testvectors with entirely customizable settings and parameters, making it ideal for FPGA system testing.

- ![CLI Diagram](./assets/Functional_Diagram.png)

## Index

- [Requirements](#requirements)
- [Connecting Devices](#connecting-devices)
- [Checking Devices' Models](#checking-devices'-models)
- [How to Access the CLI](#how-to-access-the-cli)
- [Initial Commands](#initial-commands)
- [Controllers](#controllers)
- [Resourcers](#resourcers)
- [Services](#services)
- [Waveform Control](#waveform-control)
- [Scope Control](#scope-control)
- [Testvector](#testvector)

## Requirements

To add the CLI python required modules in your virtual environment, open the project's root directory in the terminal and use the following command:

```sh
pip install -r requirements.txt
```

## Which devices is the CLI compatible with?

This CLI enables control of waveform generators and oscilloscopes compatible with the **VISA** communication protocol.

Many devices on the market support **VISA**, making them compatible with this CLI.

To control devices, connect them to your computer's USB ports. The CLI supports the connection of multiple devices simultaneously.

Even without connecting any devices, you can still access the CLI and generate test vectors via the virtual resources, that can be added via the CLI or manually using any of the virtual resources json templates found in the folder **./test_vector_control/json_templates** and placing the custom json in the folder **./data/virtual_resources/**.

Other necessary configurations will be managed within the CLI and explained further.

## Checking Devices' Model

This CLI is tailored for controlling the **Keysight 33500B Waveform Generator** and the **Tektronix MSO2024 Oscilloscope**.

If these are your intended devices, no specific parameters or command syntax need to be specified, as they are already standardized.

See if other models' command syntax matches those in the **device_specific_commands.py** (**scope_control** or **waveform_control** folders).

To confirm the correct syntax for controlling an oscilloscope, search online about the **VISA** protocol or contact the manufacturer.

If the syntax differs from that in the **device_specific_commands.py files**, you'll need to edit these files accordingly and added your own custom controller, which you can fork add/modify following the structure given by the chosen base controller.

## How to Access the CLI?

To access the CLI, download this repository and install the requirements as explained in the final section. Also, it is necessary to add this project's root directory to the PYTHONPATH of your system.

Navigate to this project's root directory in your terminal then
run the Python script to start using the CLI:

```sh
python periclis.py
```

Once it is done, the CLI is ready for immediate use!

## Initial Commands

After following the previous sections' instructions, you should already be in the CLI on your terminal.

Several initial commands are available, including:

- list_resources
- list_controllers
- connect_resource, args: ResourceId ControllerName
- disconnect
- list_commandsk
- list_servicest
- exit

The **list_controllers** and **list_resources** commands list controllers and resources, respectively (explained further in subsequent sections).

The **connect_resource** command allows connecting to a controller with a specific resource.

The **disconnect** command disconnects the current controller and resource.

The **list_commands** command allows you to see all available commands.

The **list_services** command lists all services usable on the connected controller.

The **exit** command finishes executing the **periclis.py** script, returning to the **periclis_instrumentation_controller** directory.

## Controllers

Controllers are simply sets of functionalities that you want your code to execute.

These functionalities can be:

- Control a waveform generator of electrical signals (**WaveformController**)
- Control an oscilloscope (**ScopeController**)
- Simulating voltage values and comparing them with predefined values to generate test vectors (**TestvectorController**).

In order to dynamically see all controllers available, you can use the command mentioned in the previous section:

```sh
list_controllers
```

This command will show a list containing the 3 controllers cited above:

```sh
ControllerID     ControllerName
        0       WaveformController
        1       ScopeController
        2       TestVectorController
```

Functionality of each of the above controllers' will be detailed in their directory's README.md files.

In order to access any of the controllers, you must also connect with a resource. To connect with both the controller and the resource, you can use the **connect_resource** command.

An example of this connection will be given below, to demonstrate the connecting to the **WaveformController** with the resource 0:

```sh
connect_resource 0 WaveformController
```

To connect with other controllers, such as the **ScopeController** or the TestvectorController, you can simply write their names (listed in the ControllerName row) in the command showed above, instead of **WaveformController**.

To switch to a different resource, input its corresponding number, instead of 0 (in the **connect_resource** command). Each resource is assigned a unique number (ResourceID), as detailed in the following section.

## Resources

Resources are the devices or configuration settings that are going to be used in the controllers.

In order to use a controller, you'll need usually to inform which resource/device you want to control.

This information is provided by the **VISA ID**, unique to each equipment compatible with the **VISA** communication protocol.

When the controller is connected to the TestVectorController, there are many configurations to be set.

These configurations are defined into files (formats such as .json) that act as resources. Therefore, in order to generate the test vectors, you also need to inform the resource files containing the configurations.

A list containing all existing resources, can be accessed with the following command:

```sh
list_resources
```

This command will print a list with all possible resources:

```sh
ResourceID   ResourceLabel
    0      USB0::1689::888::C010837::0::INSTR
    1      USB0::2391::9479::MY57100781::0::INSTR
    2    waveform_generators/basic_generator.json
```

In order to connect to a specific resource, you need to inform their ResourceID as shown in the table above, in **connect_resource** command, as explained in the previous section.

The resources above are dynamically actualized in the CLI, each time that a command related to them is used.

As explained, there are 2 types of resources:

- Resources of **VISA IDs**. These IDs correspond to all **VISA** devices connected to USB ports.
- Resources of configuration files that are going to be used to generate the test vectors (will be better explained in the README.md of Testvector repository).

## Services

After connecting to a controller with a defined resource, you will be able to use the specific services of the controller.Services are simply functionalities that can be used in a specific controller.

**All tasks executed by the CLI are services (including the ones with the waveform generator, oscilloscope, and the generation of test vector).** Hence, you will need to use them to perform your desired activities.

In order to check all the services of a specific controller, you must first connect to the controller with the **connect_resource** command explained above and then use the command:

```sh
list_services
```

This will return a list with all commands available for that controller. If you connect to the **WaveformController**, the CLI will return the following list with its services:

```sh
    - query_info
    - read_all
    - read_voltage
    - read_frequency
    - read_offset
    - read_phase
    - read_function_type
    - change_voltage
    - change_frequency_hz
    - change_offset
    - change_phase
    - change_function_type
```

**All services of all controllers have their functionality explained in the README.md files of each controller directory. Check these files, to understand what exactly each service can do.**

Then, you can choose the service of interest and type the command in the CLI in order to access its functionality.

For instance, the **WaveformController** has a service called **read_all** (as can be seen in the above list) which reads several parameters of the waveform generator.

You can type it in the CLI (after connected to the **WaveformController** with the **connect_resource** command as explained before) in order to access the service functionality, as shown below:

```sh
read_all
```

This service prints the following line in terminal:

```sh
"SIN +1.000E+03,+2.000E+00,+1.000E+00"
```

These data correspond to the following parameters of the waveform generator: wave format (SIN = sinusoid), frequency (1.000E+03 = 1000 Hz), amplitude (2.000E+00 = 2 V), offset (1.000E+00 = 2 V).

Another example can be given by the service **change_voltage** (also, of the **WaveformController**). This command changes the generator's voltage value to the number written after it (in Volts). An example is shown below:

```sh
change_voltage 3.0
```

The command above changes the waveform generator's voltage to 3.0 V.

It is important to reaffirm that each service is described in the README.md files of their respective directories, and **these descriptions include instructions as to when it is necessary to add variables after the commands.**
