from sh import Command as ShCommand, CommandNotFound

from .base import BaseShCommand, find_path

defaut_config = dict()

class Command(BaseShCommand):
    def __init__(self, **kwds):
        '''
        An mpv command
        '''
        super().__init__()

        try:
            self._cmd = ShCommand("mpv") # does it need to be configurable?
        except CommandNotFound:
            self._status = "No 'mpv' command found, install 'mpv' package"
            return
        except Exception as e:
            self._status = f"Unexpected error for 'mpv': {e}"
            return

    def play(self, filename):
        self(filename)
