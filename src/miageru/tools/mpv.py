from .base import BaseShCommand, find_path

defaut_config = dict()

class Command(BaseShCommand):
    def __init__(self, **kwds):
        '''
        An mpv command
        '''
        super().__init__("mpv")

    def play(self, filename):
        self(filename)
