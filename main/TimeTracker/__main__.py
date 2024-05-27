import argparse
import sys
from TimeTracker.src.commands import Commands

processed_args = []
for arg in sys.argv[1:]:
    if arg.startswith('-') and not arg[1:].isdigit() and len(arg) > 1:
        processed_args.append('--')  # Add separator to treat following arguments as positional
    processed_args.append(arg)

parser = argparse.ArgumentParser()
parser.add_argument("command")
parser.add_argument("args", nargs="*", default=[])
parsed_args = parser.parse_args(processed_args)

Commands.run_command(parsed_args.command, parsed_args.args)
