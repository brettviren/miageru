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
import importlib

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

def known_tool_names():
    for loader, module_name, is_pkg in pkgutil.iter_modules(tools.__path__):
        if is_pkg:
            continue
        module = importlib.import_module(f'miageru.tools.{module_name}')
        if hasattr(module, 'Command'):
            yield module_name

def with_method(tool_list, method_name):
    return [t for t in tool_list if hasattr(t, method_name)]

def get_class(name):
    #mod = import_module(name, miageru.tools)
    mod = importlib.import_module(f".tools.{name}", package=__package__)
    return mod.Command

def get_command(name, **cfg):
    Command = get_class(name)
    return Command(**cfg)

def get_method(meth, tool, cfg={}):
    obj = get_command(tool, **cfg)
    return getattr(obj, meth)


def get_tool_module(module_name, default=None):
    '''
    Return tool module.
    '''
    # First try as on of our tool modules
    try:
        return importlib.import_module(f'miageru.tools.{module_name}')
    except ModuleNotFoundError:
        pass

    # Next, try as a stand-alone
    try:
        return importlib.import_module(module_name)
    except ModuleNotFoundError:
        pass
                
    return default

class Methods:
    '''
    Map user configuration to tools to use for methods.

    The config maps a tool instance name to its config, and possibly the module
    providing the tool class.

    The tools list, if given, limits the tools to be considered.
    '''

    def __init__(self, cfg=None, tools=None):
        cfg = cfg or {}

        self._cfg_method = cfg.get("method", {})
        self._cfg_tool = cfg.get("tool", {})
        self._allowed_tools = tools

        # cache
        self._methods = dict()
        self._tool_modules = None

    def _allowed(self, tool_name):
        return not self._allowed_tools or tool_name in self._allowed_tools

    def iter_tools(self, lst = None):
        def iter_all():
            if lst is not None:
                for one in lst:
                    yield one
            for one in self._cfg_tool.keys():
                yield one
            if self._tool_modules is None:
                self._tool_modules = list(known_tool_names())
            for one in self._tool_modules:
                yield one
        for one in iter_all():
            if self._allowed(one):
                yield one

    def _first_method_with(self, method_name, user_tool_list=None, default=None):
        for tool_name in self.iter_tools(user_tool_list):
            tool_cfg = self._cfg_tool.get(tool_name, {})
            module_name = tool_cfg.get("module", tool_name)
            mod = get_tool_module(module_name)
            if mod is None:
                continue
            if not hasattr(mod, 'Command'):
                continue
            if not hasattr(mod.Command, method_name):
                continue
            cfg = self._cfg_tool.get(tool_name, {})
            return getattr(mod.Command(**cfg), method_name)
        return default
            

    def get(self, method_name, default=None):
        '''
        Return a method of the name subject to selection rules.
        '''
        # first check if we've been here before
        tool = self._methods.get(method_name, None)
        if tool is not None:
            return tool

        # Resolve method name given tool ordering
        method_tool_list = self._cfg_method.get(method_name, {}).get("tools", None)
        meth = self._first_method_with(method_name, method_tool_list)
        if meth is None:
            return default
        
        self._methods[method_name] = meth
        return meth

    def __getattr__(self, method_name):
        meth = self.get(method_name)
        if meth is None:
            raise KeyError(f'no method "{method_name}"')
        return meth

    def transcode(self, src_file, dst_file):
        '''
        Transcode one audio file to another by matching by extensions.
        '''
        src = src_file.suffix[1:]
        dst = dst_file.suffix[1:]

        name = f'{src}_to_{dst}'
        tc = find_method(name, self._cfg_tool, self._preferred_tool(name))
        tc(src_file, dst_file)
        
