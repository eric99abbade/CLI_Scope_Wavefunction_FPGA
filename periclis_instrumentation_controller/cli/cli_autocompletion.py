# DAT/EMI - Electronics and Microelectronics Department
# Redistribution, modification or use of this software in source or binary
# forms is permitted as long as the files maintain this copyright. 

###############################################################################
# DAT/EMI and the Brazilian Center for Research in Energy and Materials (CNPEM)
# are not liable for any misuse of this material.
#
# @file cli_autocompletion.py
#
# @brief CLI for controlling OScilloscope, Wavegenerator and TestVector.
#
# @author Pedro Trindade 
# @author Eric Sonagli Abbade.
# @date 24/04/2024
###############################################################################

from functools import partial 

# Avoiding type hinting cyclic import  
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cmd_base import CMDBase 

#@TODO fix autocompletion
class CMDAutocompletion:   
    def complete_command(self, command_options : list[str], text, line, start_index, end_index):
        """
            This is the default template method that needs to be added to the CMD 
            object to autocomplete a given command.
        """
        if text: # if I already started typing the option, filter the existing options
            return [
                option for option in command_options
                if option.startswith(text)
            ]
        else:
            return command_options
        
    def completedefault(self, commands : list[str], text, line, begidx, endidx):
        if not text:
            completions = commands[:]
        else:
            completions = [command for command in commands if command.startswith(text)]
        return completions
    
    def add_cmd_autocompletion(self, cmd : "CMDBase", command_list : list[str]):
        autocomplete_options = [controller for controller in cmd.available_controllers] 

        ## Set the tab for added services
        self.set_root_autocompletion(cmd, command_list)
        
        for command_name in command_list:
            self.add_autocompletion(cmd, command_name, autocomplete_options)
        
    def set_root_autocompletion(self, cmd : "CMDBase", 
                                complete_options : list[str]):
        setattr(cmd, 'completedefault', partial(self.completedefault, complete_options))

    def add_autocompletion(self, cmd : "CMDBase", 
                           command_name : str, command_options : list[str]):
        """
        This function dynamically adds autocompletion support in the Cmd Module
        for a command with specified options in a Python class.
        """
        setattr(cmd, 'complete_' + command_name,
                partial(self.complete_command, command_options))