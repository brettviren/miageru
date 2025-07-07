from pathlib import Path
def find_path(filename, paths = (), default=None):
    '''
    Return Path object for file, search paths if necessary.  Return default
    value if filename is not found
    '''
    path = Path(filename)

    if path.exists():
        return path
    for maybe in paths:
        p = Path(maybe) / path
        if p.exists():
            return p
    return default

class BaseShCommand:
    '''
    Boilerplate mixin for sh using Command
    '''
    def __init__(self):
        self._cmd = None
        self._status = None

    def __bool__(self):
        return self._cmd is not None

    def __str__(self):
        return self._status

    def __call__(self, args, **kwds):
        if not self:
            raise RuntimeError(f"Can not call {self}.  Status:\n{self}")
        return self._cmd(args, **kwds)
    
