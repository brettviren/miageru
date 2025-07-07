#!/usr/bin/env -S uv run --script
# -*- python -*-
# /// script
# dependencies = ["click"]
# ///

import click
from pathlib import Path

from miageru.database import open_db

class Context:
    def __init__(self, dbfile):
        self.dbfile = dbfile

    def connect(self):
        return open_db(self.dbfile)

    def find_term(self, term, service=None):


@click.group()
@click.option("--db", default=Path.home() / "miageru.db")
@click.pass_context
def cli(ctx, db):
    '''
    Look up and process terms.
    '''
    ctx.obj = Context(db)


@cli.command("say")
@click.option("-s","--service", click.Choice("jtalk", "google", "espeak-ng"),
              help="What service to use to say the term.")
@click.option("-o","--output", default=None, type=str,
              help="How to output result, default will play else write file")
@click.option("-f","--force", is_flag=True, default=False,
              help="Force to use service and rewrite term entry")
@click.argument("term", nargs=-1)
@click.pass_context
def cli_say(ctx, service, output, term):
    '''
    Say a term.
    '''
    term = ctx.obj.get_term(' '.join(term), service)

if __name__ == '__main__':
    cli()
