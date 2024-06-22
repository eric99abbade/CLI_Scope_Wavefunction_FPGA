from periclis_instrumentation_controller.utils.color_handling import *
from periclis_instrumentation_controller.cli.periclis_cli import PericlisCmd

def main():
    my_cmd = PericlisCmd()
    my_cmd.cmdloop()

if __name__ == '__main__':
    main()