from sh import Command as ShCommand, CommandNotFound

from .base import BaseShCommand

default_config = dict(
    host=None,
    port=None,
    db="fd-jpn-eng",  # limit to a single db
)

class Command(BaseShCommand):
    def __init__(self, db=None, host=None, port=None, **kwds):
        '''
        oggenc
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



