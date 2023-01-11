import sys
from inspect import getmembers, isfunction

from wsgi_framework import commands

help_command = "help"
commands_dict = dict(getmembers(commands, isfunction))


def get_help():
    print("Usage: python manage.py [command] [args]")
    print("Available commands:")
    print(*sorted(commands_dict.keys()), sep="\n")


commands_dict.update({help_command: get_help})


if __name__ == "__main__":
    try:
        input_command = sys.argv[1]
        params = sys.argv[2:]
        commands_dict[input_command](*params)
    except (KeyError, IndexError):
        commands_dict[help_command]()
