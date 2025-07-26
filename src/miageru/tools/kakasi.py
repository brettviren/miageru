from .base import BaseCommand, find_path


default_config = dict()

class Command(BaseCommand):
    '''
    Call the pykakasi kanji/kana/romaji converter.

    Returns list of dicts with keys orig, hira, kana, hepburn, etc.
    '''

    def __init__(self, primary=True, **kwds):
        super().__init__()

        try:
            import pykakasi
        except ImportError:
            self._status='No pykakasi package'
            return
        kks = pykakasi.kakasi()
        self._cmd = kks.convert
        self._status = f'pykakasi kanji/kana/romaji converter is available'
    def read(self, terms, **kwds):
        '''
        Return hiragana.  This is neither very useful nor trustworthy.
        '''
        parts = list()
        for term in terms:
            parts += [t['hira'] for t in self._cmd(term)]
        return ' '.join(parts)
        
