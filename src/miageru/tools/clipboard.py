from .base import BaseShCommand, find_path

default_config = dict(
    primary = True
)

class Command(BaseShCommand):
    def __init__(self, primary=True, **kwds):
        super().__init__()

        try:
            import pyperclip
        except ImportError:
            self._status='No pyperclip package'
            return
        self._cmd = pyperclip.paste
        self._primary = primary
        self._status = f'pyperclip paste available'

    def __call__(self, *args, primary=None, **kwds):
        '''
        Return what is in the clipbard
        '''
        if primary is None:
            primary = self._primary
        return self._cmd(primary=primary)
