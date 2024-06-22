## Test Vector Controller

## Brief Description
This folder implements the Test Vector Controller for **test vector virtual resources**. Contains a service (test) the generates a test vector file (.json). This file stores the values of voltage simulations (both in analog and digital format) and compares them with a voltage interval. The comparison results in an output that says whether the voltage is inside (true) or outside (false) the interval.


## Connecting the Resource
You can use Resources (.json configuration files) for generating the test vector (another .json file with the simulated voltages).

As explained in the README.md (of the periCLIs Instrumentation Controller), you can connect to a waveform generator with:

```sh
connect_resource 0 TestVectorController
```

If the ResourceID differs from 0, substitute its value in the command above.

## Understanding the JSON Configuration Resource
The standard JSON Configuration Resource has the following parameters (their respective meanings are on the right side):

- **"min_voltage":** minimal value possible of the voltage.
- **"max_voltage":** maximal value possible of the voltage.
- **"threshold_voltage":** maximal value of voltage that is accepted and generates a true output.
- **"voltage_offset":** voltage offset of the signal.
- **"bit_resolution":** number of bits used in the discretization of the signal.
- **"signed":** false,
- **"fixed_point_representation":** [7, 5],
- **"number_inputs":** number of input voltages to be measured.
- **"number_samples":** numbers of samples of measured voltages.
- **"sampling_period":** interval period of the voltage measures.
- **"wave_type":** wave format (ex: sine).
- **"frequency":** frequency of the wave.


**Services:** typing commands on the terminal, which work after establishing the connection with the TestVectorController in the last section.

Type any of the commands (services) below after connecting with the controller (the **bold** values in parentheses are user-defined inputs):
- **new_resource**, args: json_file_name (.txt or .json)
- **delete_resource**, args: json_file_name_to_delete
- **change_resource_config**, args: configuration_variable_name, configuration_variable_new_value
- **copy_resource**, args: json_file_name_to_receive_resource_copy
- **read_resource_configs**
- **generate_testvector**
- **plot_testvector**
- **save_testvector**, args: out_file_name (opt)
- **delete_testvector**, args: file_name_to_delete
- **list_testvectors**

<br></br> 

You can view the list above in the CLI after typing the following (if connected to the controller):

```sh
services_list
```

You can type the following service (or any from the list above) command in the terminal after connecting to the controller:

```sh
generate_testvector
```

This will generate a JSON file with the voltage values (analog and digital), and their outputs (true if below threshold; false otherwise). <br></br>

To save this JSON file (in an example.json file), type:
```sh
save_testvector example.json
```
If you do not use the "example.json" in the end, the file is going to be saved with a pre-defined name.

You can also print the simulated voltage with: 
```sh
plot_testvector example.json
```
<br></br>
Following this logic, all list service commands can be utilized. Below is a description of each command's functionality:
- **new_resource** creates a new JSON file (with name defined by the "json_file_name" argumment) that can be used as a Resource.
- **delete_resource** deletes file (with name defined by the "json_file_name_to_delete" argumment).
- **change_resource_config** edits a configuration parameter named with the c"onfiguration_variable_name" argument to the value of the "configuration_variable_new_value" argument on a resource file.
- **copy_resource** copy resource configurations to the file named by the "json_file_name_to_receive_resource_copy" argumment.
- **read_resource_configs** prints the parameters of the connected resource file.
- **generate_testvector** generates a JSON file with the voltage values and their respective output (true or false).
- **plot_testvector** prints an image with the wave of the simulated voltage*
- **save_testvector**, args: ['out_file_name (opt)'] saved the data of the voltage simulated values.*
- **delete_testvector**, args: ['file_name_to_delete (opt)'] deletes one resource (type its name after the command).
- **list_testvectors** lists the testvector files with the simulated voltage values.







