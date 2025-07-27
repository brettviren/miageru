from .base import BaseShCommand, find_path

defaut_config = dict()

class Command(BaseShCommand):
    def __init__(self, **kwds):
        '''
        Interface to the mecab command
        '''
        super().__init__("mecab")

    def split(self, text):
        '''
        Return text split into words.
        '''
        words = list()
        for line in self._cmd(_in=text).split("\n"):
            if line.startswith("EOS"):
                return words
            word, _ = line.split(maxsplit=1)
            words.append(word)
        return words

