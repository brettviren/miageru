from sh import Command as ShCommand, CommandNotFound
from pathlib import Path
from .base import BaseShCommand

class Command(BaseShCommand):
    def __init__(self, **kwds):
        super().__init__("oggenc")

    def wav_to_ogg(self, wav_file, ogg_file = None):
        if ogg_file is None:
            ogg_file = wav_file.replace('.wav','.ogg')
        self._cmd('-o',  ogg_file, wav_file)
        return Path(ogg_file)
