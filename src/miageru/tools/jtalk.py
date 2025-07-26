from importlib import resources
from pathlib import Path
from .base import BaseShCommand, find_path

default_config = dict(
    dictdir="/var/lib/mecab/dic/open-jtalk/naist-jdic",
    voicepath=[], # also checks built in
    voice=None, # "tohoku-f01-neutral.htsvoice",
    name="tohoku",
    personality="neutral",
    halftone=1.0,               # -fm
    rate=1.0,                  # -r
)

class Command(BaseShCommand):
    def __init__(self,
                 dictdir="/var/lib/mecab/dic/open-jtalk/naist-jdic",
                 voice=None, voicepath=None,
                 name="tohoku", personality="neutral",
                 halftone=None, rate=None, **kwds):
        '''
        An Open JTalk command
        '''
        super().__init__("open_jtalk")

        # get just version info not CLI help
        lines = list()
        for line in self._cmd().split("\n"):
            if 'usage:' in line:
                break
            lines.append(line)
        self._status = '\n'.join(lines)

        # figure out voice file
        known = dict(mei = f'mei_{personality}.htsvoice',
                     tohoku = f'tohoku-f01-{personality}.htsvoice')
        if voice is None:
            voice = known[name]
        voicepath = voicepath or list()
        voicepath += list(resources.files("miageru.data.voices").iterdir())
        voice = str(find_path(voice, voicepath))

        # bake options
        opts = []
        if dictdir is not None:
            opts += ["-x", dictdir]
        if voice is not None:
            opts += ["-m", voice]
        if halftone is not None:
            opts += ["-fm", halftone]
        if rate is not None:
            opts += ["-r", rate]
        self._cmd = self._cmd.bake(opts)

    def __call__(self, text, wavfile, *args, **kwds):
        '''
        Call Open JTalk with some text and a .wav file to receive the voice.
        '''
        if not self:
            raise RuntimeError(f"Can not call {self}.  Status:\n{self}")
        self._cmd("-ow", wavfile, args, _in=text, **kwds)
        return wavfile


    def tts(self, text, *args, **kwds):
        import tempfile
        fp = tempfile.NamedTemporaryFile(suffix=".wav")
        fp.close()
        self(text, fp.name)
        return Path(fp.name)

