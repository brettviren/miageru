#!/usr/bin/env python
from .base import BaseCommand
import socket

default_config = dict()

class Command(BaseCommand):
    '''
    lookup terms from a dictd server using a raw sockets.
    '''
    def __init__(self, db=None, host="localhost", port=2628, **kwds):
        super().__init__()

        if not db:
            db = "!"

        def lookup(word):
            command = f"DEFINE {db} {word}\r\n"
            print(f'{command=}')

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                response_lines = []
                s.connect((host, port))
                s.sendall(command.encode('utf-8'))

                while True:
                    data = s.recv(4096).decode('utf-8', errors='ignore')
                    print(f'{data=}')
                    if not data:
                        break
                    response_lines.append(data)
                    # Simple heuristic to detect end of response for DEFINE:
                    # Look for "250 ok" or "552 no match" lines,
                    # or if the socket closes (no more data).
                    if "250 ok" in data or "552 No match" in data:
                        break
                response = "".join(response_lines)

            lines = list()
            for line in response.split("\r\n"):
                print(f'{line=}')
                first = line.split()[0]
                if first in ("220", "150", "151"):
                    # skip unwanted headers.  
                    continue
                if first == "250": # end
                    break
                lines.append(line)
            return '\n'.join(lines)
                
        self._cmd = lookup
        self._status = "raw dict client lookup available"

    def dictionary(self, term):
        '''
        Return multiline string with dictionary definition of term.
        '''
        return self(term)
