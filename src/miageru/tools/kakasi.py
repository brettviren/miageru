from .base import BaseCommand


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

    def kakasi(self, terms, **kwds):
        return [self._cmd(term) for term in terms]

    def spelling(self, terms, **kwds):
        for term in terms:
            print(self._cmd(term))

    def furigana(self, terms):
        '''
        Return words with any kanji word appended with [furigana].

        Caller should take care to split words properly.  
        '''
        words = list()
        for term in terms:
            # kakasi will still split at kanji boundaries
            for kk in self._cmd(term):
                orig = kk['orig']
                if kk['kana'] == orig:
                    words.append(orig)
                    continue
                hira = kk['hira']
                if hira == orig:
                    words.append(orig)
                    continue
                words.append(f'{orig}[{hira}]')
        return words
