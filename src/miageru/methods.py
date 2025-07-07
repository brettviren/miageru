'''
modules:
- pyperclip for xclip
- googletrans for translation-shell
- gtts for text-to-speech
- deepl / deep-translator also?
- pydub for audio conversion
- simpleaudio for playing
- pykakasi for kanji -> hiragana <--> katakana <--> hepburn

programs:
- dict
- open_jtalk for text-to-speech
- rofi

unsure
- genanki instead of trrc?


Tool rules:

One module for each low level tool.  Each module is expected to import'able even
if the environment lacks what it may need to run.  The module must provide the
following:

default_config a dictionary that can be converted to toml with default config values

class Command with:

- constructor taking keyword args.  

- a __bool__() method returning False if the command can not function

- a __str__() method giving version strings or other identifiers or error message if false.  If the Command is an sh command, include the string rep of that object as first line.

- a __call__() method to do the command with Command-specific args

- additional "action" methods each with common calling defined in actions.

'''

import pkgutil
from . import tools
def known_tools():
    #= [n for _, n, _ in pkgutil.iter_modules(tools.__path__)]

    submodule_names = list()
    for loader, module_name, is_pkg in pkgutil.iter_modules(tools.__path__):
        if is_pkg:
            continue
        module = importlib.import_module(f'miageru.tools.{module_name}')
        if hasattr(module, 'Command'):
            submodule_names.append(module_name)
    return submodule_names

import importlib

def get_class(name):
    #mod = import_module(name, miageru.tools)
    mod = importlib.import_module(f".tools.{name}", package=__package__)
    return mod.Command

def get_command(name, cfg):
    Command = get_class(name)
    return Command(**cfg)

def get_method(meth, tool, cfg={}):
    obj = get_command(tool, **cfg)
    return getattr(obj, meth)

def find_method(meth, cfg={}, tool=None):
    if tool:
        return get_method(meth, tool, cfg)

    for name in known_tools():
        Command = get_class(name)
        if hasattr(Command, meth):
            return getattr(Command(**cfg), meth)
    raise RuntimeError(f'no method {meth} available')

class Methods:
    '''
    Map user configuration to tools to use for methods.
    '''

    def __init__(self, cfg = {}):
        self._cfg = cfg
        # fixme: use cfg to mitigate method lookup
        # for now, wing it

    def _prefered_tool(self, name):
        # fixme: dig into cfg to see if user has a preferred tool for method
        return None

    def __getattr__(self, name):
        
        return find_method(name, self._cfg, self._prefered_tool(name))
