from periclis_instrumentation_controller.cli.str_formatting import *
from periclis_instrumentation_controller.cli.cmd_base import CMDBase
from periclis_instrumentation_controller.utils.color_handling import *

class PericlisCmd(CMDBase):
    def __init__(self) -> None:
        super().__init__()

if __name__ == '__main__':
    my_cmd = PericlisCmd()
    my_cmd.cmdloop()

#periclis < ./scripts/test.txt