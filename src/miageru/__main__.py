#!/usr/bin/env -S uv run --script
# -*- python -*-
# /// script
# dependencies = ["click"]
# ///

import click
from pathlib import Path
from miageru.methods import Methods

# todo: dump config


@click.group()
@click.option("--db", default=Path.home() / "miageru.db")
@click.pass_context
def cli(ctx, db):
    '''
    Look up and process terms.
    '''
    ctx.obj = None # Context(db)
    # todo: load config


@cli.command("say")
@click.option("-o","--output", default=None, type=str,
              help="How to output result, default will play else write file")
@click.argument("term", nargs=-1)
@click.pass_context
def cli_say(ctx, output, term):
    '''
    Say a term.
    '''
    cfg = {}                    # fixme, get this from context
    m = Methods(cfg)

    # fixme: make a class that is configured to pick services the user prefers
    # and presents all methods. for now, just get something working
    tmpfile = m.tts(term)
    if not output:
        m.play(tmpfile)

    else:
        # fixme: do conversion if needed
        print(tmpfile)
        



if __name__ == '__main__':
    cli()
