from .base import BaseShCommand, find_path


default_config = dict()

class Command(BaseShCommand):
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

