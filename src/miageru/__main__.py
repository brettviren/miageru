#!/usr/bin/env -S uv run --script
# -*- python -*-
# /// script
# dependencies = ["click"]
# ///

import click
import shutil
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
@click.option("-o","--output", default=None, type=Path,
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
        tmpfile.unlink()
        return

    if tmpfile.suffix == output.suffix:
        shutil.move(tmpfile, output)
        return
    print(tmpfile, output)
    m.transcode(tmpfile, output)

@cli.command("read")
@click.option("-o","--output", default=None, type=Path,
              help="Output to file, else stdout")
@click.argument("term", nargs=-1)
@click.pass_context
def cli_read(ctx, output, term):
    '''
    Provide reading for a phrase.
    '''
    cfg = {}                    # fixme, get this from context
    m = Methods(cfg)
    reading = m.read(term)
    if not output:
        print(reading)
        return
    Path(output).write_text(reading)

if __name__ == '__main__':
    cli()
