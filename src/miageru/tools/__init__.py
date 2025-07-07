'''
modules:
- pyperclip for xclip
- googletrans for translation-shell
- deepl / deep-translator also?

programs:
- dict
- rofi

unsure
- genanki instead of trrc?

'''

# One module for each low level tool.  Each module is expected to import even if
# the system lacks what it needs.  The module must provide the following:
#
# .default_config a dictionary that can be converted to toml with default config values
#
# Command class with:
#
# - constructor taking keyword args.  It will be given the content of the TOML flie
#
# - a __bool__() method returning False if the command can not function
#
# - a __str__() method giving version strings or other identifiers or error message if false.  If the Command is an sh command, include the string rep of that object as first line.
#
# - a __call__() method to do the command with Command-specific args
#
# - any additional command-specific methods

from . import dictc

