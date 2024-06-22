# DAT/EMI - Electronics and Microelectronics Department
# Redistribution, modification or use of this software in source or binary
# forms is permitted as long as the files maintain this copyright. 

###############################################################################
# DAT/EMI and the Brazilian Center for Research in Energy and Materials (CNPEM)
# are not liable for any misuse of this material.
#
# @file file_parsing.py
#
# @brief CLI for controlling OScilloscope, Wavegenerator and TestVector.
#
# @author Pedro Trindade 
# @author Eric Sonagli Abbade.
# @date 24/04/2024
###############################################################################

from periclis_instrumentation_controller.utils.color_handling import *
from periclis_instrumentation_controller.utils.errors_handling import *
from periclis_instrumentation_controller.utils.variable_rules import test_value #Variable_Rules

import os
import json
from pathlib import Path
import logging
import csv 


def add_config(new_data, file_path, extension: str, restrictions = None):
    if extension == '.json' or extension == '.csv':        
        for restriction in restrictions: #In case there are restrictions:
            file_data = read_file(file_path, extension) # Read existing aliases or create an empty list.
            file_data = check_similarites(new_data[restriction], file_data, extension, str(restriction))
            write_file(file_data, file_path, extension) #Adds new alias data.   
        file_data.append(new_data) #Appends new data. 
        write_file(file_data, file_path, extension) #Adds new alias data. 
    else:
        raise ValueError("Unsupported file format.")
    
def check_similarites(new_data, file_data, extension: str, restriction = None, message: str = None): #Checks if there is already something saved with a similar value.
    if extension == '.json':
        new_data_corrected = []        
        for item in file_data:
            if item[restriction] != new_data:
                new_data_corrected.append(item) #Appends new data.
            else:            
                if message:
                    print_yellow(message) #If there is another message, it will be printed.
                else: #Standard message
                    print_yellow(f"The {restriction} with value of {new_data} is already stored on file. This new alias will overwrite the previous!")
        return new_data_corrected
    else:
        pass

def erase_config(erase_data, file_path, extension: str, name_erase_data):
    if extension == '.json':
        file_data = read_file(file_path, extension) # Read existing aliases or create an empty list.
        string_erased = f"The {name_erase_data} with value of {erase_data} was successfully erased!." #Message, to denote that data was erased.
        new_data_corrected = check_similarites(erase_data, file_data, extension, name_erase_data, string_erased)
        if file_data == new_data_corrected:
            print_yellow(f"None data corresponding to {name_erase_data} {erase_data} for being erased!")
        write_file(new_data_corrected, file_path, extension) #Rewrites corrected data.
    else:
        pass    

def read_file(file_path, extension: str):
    if extension == '.json':
        if not os.path.exists(file_path):
            return []  # Return an empty list if the file doesn't exist
        with open(file_path, 'r') as file:
            return json.load(file)
    elif extension == '.csv':
        with open(file_path, "r", newline='') as csvfile:
            data_read = csv.DictReader(csvfile)
            dict = {}
            for row in data_read: # Iterate over each key-value pair in the row dictionary                          
                dict[row['name']] = row['value']
            return dict            
    else:
        raise ValueError("Unsupported file format.")

def write_file(data, file_path, extension: str, fieldnames:list=['name', 'value']):
    if extension == '.json':
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    elif extension == '.csv':
        with open(file_path, 'w', newline='') as csvfile:
            if isinstance(data, dict):
                write_dict_csv(csvfile, data, fieldnames)
            elif isinstance(data, list):
                write_list_csv(csvfile, data, fieldnames)
            else: 
                raise Exception("Error in the data format sent to csv file.")
    else:
        raise ValueError("Unsupported file format.")
    
def write_dict_csv(csvfile, data: dict, fieldnames:list=['name', 'value']):
    writer = csv.DictWriter(csvfile, fieldnames)
    writer.writeheader()        
    for key, value in data.items():
        writer.writerow({str(fieldnames[0]): key, str(fieldnames[1]): value})

def write_list_csv(csvfile, data: list, fieldnames:list=['name', 'value']):
    writer = csv.writer(csvfile)
    writer.writerows(data)

def update_file(data_to_write, file_path_to_read, extension: str, controller: str = None):
    current_data = read_file(file_path_to_read, extension)
    update = []
    for new_name, new_value in data_to_write.items():
        for attr_name in current_data.keys(): 
            if attr_name == new_name:   
                current_data[attr_name] = equalize_type(new_value, current_data[attr_name])
                update.append(current_data[attr_name]) #Armazenes the modifications. 
    if update:
        write_file(current_data, file_path_to_read, extension, ['name', 'value'])
    return update

def print_configurations(file_dir: Path, file_name: str, extension: str):
    print_green("\n> Resource Configuration Values:\n")
    data = read_file((file_dir / Path(file_name+extension)), extension)
    for row in data: # Iterate over each key-value pair in the row dictionary  
        print(f"{row} = {data[row]}")

def change_specific_configuration(self, update_data: list, file_dir, file_name: str, extension: str, device, controller: str = None):
    change_file (self, update_data, file_dir, file_name, extension, controller)       
    convert_list_variables(self, (file_dir), (file_name + extension), extension) #Update the configuration variables. 
    device.timeout = (float(self.standard_timeout))*1000 #Sets the initial timeout.
        
def return_default_configurations(self, file_dir, file_default: str, file_name: str, extension: str, device, controller: str = None):
    data_read = read_file((file_dir / Path(file_default + extension)), extension) 
    update_file(data_read, (file_dir / Path(file_name + extension)), extension, controller) 
    convert_list_variables(self, (file_dir), (file_name + extension), extension) #Update the configuration variables. 
    device.timeout = (float(self.standard_timeout))*1000 #Sets the initial timeout.
    print_green("Returned to default configurations!")

def convert_list_variables(self, file_dir: Path, file_name: str, extension: str): #Reads variables from a list and returns Python variables for the class.      
    data = read_file(Path(file_dir/file_name), extension)
    for attr_name in data.keys():
        setattr(self, str(attr_name), data[attr_name]) #Defining variables with respectives names and values. 
    
def change_file (self, update_data: list, file_dir, file_name: str, file_format: str, controller: str = None):        
    if len(update_data) != 2:
        raise Exception("Must inform (variable name) + (variable new name) after command!")         
    test_value(self, update_data, controller) #Checks if the new variable value is inside the desired rules
    (key, value)=(update_data[0], update_data[1])        
    changed_variable = update_file({key: value}, (file_dir / Path(file_name+file_format)), file_format, controller)
    if changed_variable:
        print_green(f"Value of {update_data[0]} changed to {changed_variable[0]}") 
    else:
        print_red(f"None variable is named {update_data[0]}! Check variables name with read_configurations")

def split_file_format(string: str):
    split_index = string.rfind('.')
    if split_index != -1:
        file = string[:split_index]
        file_format = string[split_index:]
    else:
        raise Exception("Must inform the name of the file (including the folder path and the .json or the desired format at end) after command!")
    if len(file_format) < 2:
        raise Exception("Must inform the name of the file (including the folder path and the .json or the desired format at end) after command!")
    return file, file_format

def create_file(path: Path, filename: str, file_format: str):  
    file = open((str(path)+'/'+str(filename))+file_format, 'a')
    file.close()

def write_txt_from_dict(data: dict, file_path: Path):#Write Basic VHDL TestVector to File.
    try:
        with open(file_path, 'w', newline='') as output_file:
            data_keys = list(data.keys())
            writer = csv.DictWriter(output_file, fieldnames=data_keys, delimiter=' ')
            number_of_samples = len(data[data_keys[0]])
            for idx in range(number_of_samples):
                row = {key: data[key][idx] for key in data_keys}
                writer.writerow(row)
    except Exception as error: 
        logging.exception(f"Failed to write TestVector: {error}")
        raise error

def delete_file(file_path: Path):
    """Delete a file at the given path."""
    try:
        if file_path.exists():
            file_path.unlink()
        else:
            logging.exception("File does not exist.")
        return True
    except Exception as e:
        logging.exception(f"Failed to delete file: {e}")
        return False

def check_if_file_exists(file_path: Path): #Check if a file exists at the given path.
    return file_path.exists()

def checking_file_on_directory(path: Path, filename: str, file_format: str): #Check if a file exists at the given path.
    (path, filename) = split_path_before_last_slash(path, filename)
    for existing_file in list_files(path):
        if filename+file_format == existing_file:
            return True
    return False

def split_path_before_last_slash(fixed_path, analyzed_string): #Test if the string has a path contained on it and send this path to the previous path.
    if '/' not in analyzed_string: # If there is no slash in the path, return the original path and an empty string
        return fixed_path, analyzed_string
    else:
        parts = analyzed_string.rsplit('/', 1) # Otherwise, return the part before the last slash combined with the fixed path, and the part after splited.
        return Path(fixed_path/parts[0]), parts[1]

def list_files(directory_path: Path): #List all files in the given directory.
    files = []
    try:
        files = [file.name for file in directory_path.iterdir() if file.is_file()]
        return files
    except Exception as e:
        logging.exception(f"Failed to list files: {e}")
        raise e                    
