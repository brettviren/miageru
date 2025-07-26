from .base import BaseShCommand

default_config = dict(
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
    def __init__(self, db=None, host=None, port=None, **kwds):
        '''
        lookup terms using a dictd client 
        '''
        super().__init__("dict")

        opts = []
        if host:
            opts += ["--host", host]
        if port:
            opts += ["--port", port]
        if db:
            opts += ["--database", db]

        if opts:
            self._cmd = self._cmd.bake(opts)

        dblist = self._cmd('--dbs') # note, --database doesn't limit this
        if db and db not in dblist:
            self._status = 'Required dict database is missing: {db}'
            self._cmd = None
            return

        version = self._cmd('--version', _ok_code=1)
        self._status = f'{self._cmd}\n{version}\n{dblist}'

    def dictionary(self, term):
        '''
        Return multiline string with dictionary definition of term.
        '''
        text = self(term)
        # return fix_weird_text(text)
        return text


