from .base import BaseShCommand, find_path

# defaults but can override at call time
default_config = dict(
    lang='ja',
    slow=False
)

class Command(BaseShCommand):
    def __init__(self, lang='ja', slow=False, **kwds):
        super().__init__()

        try:
            from gtts import gTTS
        except ImportError:
            self._status='No gTTS package'
            return
        self._lang = lang
        self._slow = slow
        self._cmd = gTTS
        self._status = f'google text-to-speech available'

    def __call__(self, text, mp3file, *args, lang=None, slow=None, **kwds):
        '''
        Call Google text-to-speech to make mp3 file.
        '''
        if lang is None:
            lang = self._lang
        if slow is None:
            slow = self._slow

        tts_file = self._cmd(text, lang=lang, slow=slow)
        tts_file.save(mp3file)
        return mp3file
        


