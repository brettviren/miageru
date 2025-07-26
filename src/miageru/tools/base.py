from sh import Command as ShCommand, CommandNotFound, ErrorReturnCode

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

class BaseCommand:

    def __bool__(self):
        return self._cmd is not None

    def __str__(self):
        return self._status

    def __call__(self, args, **kwds):
        if not self:
            raise RuntimeError(f"Can not call {self}.  Status:\n{self}")
        return self._cmd(args, **kwds)



class BaseShCommand(BaseCommand):
    def __init__(self, program):
        self._cmd = None
        self._status = None

        try:
            self._cmd = ShCommand(program)
        except CommandNotFound:
            self._status = f'No "{program}" command found'
            return
        except Exception as e:
            self._status = f'Unexpected error for "{program}": {e}'
            return

