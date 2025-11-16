from .base import BaseShCommand

default_config = dict(
    prog="dict",
    host=None,
    port=None,
    db="fd-jpn-eng",  # limit to a single db
)

def fix_weird_word(word):
    for weird in "abbreviation colloquialism archaism".split():
        if word.startswith(weird):
            return [weird, word[len(weird):]]
    return [word]


def fix_weird_line(line):
    words = list()
    for word in line.split():
        words += fix_weird_word(word)
    return ' '.join(words)
    

def fix_weird_text(text):
    lines = list()
    for line in text.split("\n"):
        if not line.strip():
            continue
        if ' definition found' in line:
            continue
        if line.startswith('From '):
            continue
        if line[:2] == "  ":
            line = line[2:]
        line = fix_weird_line(line)
        lines.append(line)
    return '\n'.join(lines)


class Command(BaseShCommand):
    def __init__(self, db=None, prog="dict", host=None, port=None, **kwds):
        '''
        lookup terms using a dictd client 
        '''
        super().__init__(prog)

        version = self._cmd('--version', _ok_code=[0,1])
        version = version.split("\n")[0]

        print(f'DICT: {prog=} {db=} {host=} {version=}')

        opts = []
        if host:
            opts += ["--host", host]
        if port:
            opts += ["--port", port]
        if db:
            opts += ["--database", db]

        if opts:
            self._cmd = self._cmd.bake(opts)

        self._status = f'{self._cmd}\n{version}'

    def dictionary(self, term):
        '''
        Return multiline string with dictionary definition of term.
        '''
        text = self(term)
        # return fix_weird_text(text)
        return text


