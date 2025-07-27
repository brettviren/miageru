#!/usr/bin/env -S uv run --script
# -*- python -*-
# /// script
# dependencies = ["click"]
# ///

import click
import shutil
from pathlib import Path
from collections import defaultdict
from miageru.methods import Methods

# todo: dump config


@click.group()
@click.option("--db", default=Path.home() / "miageru.db")
@click.option("-t","--tools", default=None, type=str, multiple=True,
              help="Override config to set preferred tools with meth=tool arg")
@click.pass_context
def cli(ctx, db, tools):
    '''
    Look up and process terms.
    '''
    tools_cfg = defaultdict(list)
    for tool in tools:
        for more in tool.split(","):
            m,t = more.split("=")
            tools_cfg[m].append(t)

    ctx.obj = Methods(dict(tools=tools_cfg))

    # Context(db)
    # todo: load config


@cli.command("say")
@click.option("-o","--output", default=None, type=Path,
              help="How to output result, default will play else write file")
@click.argument("terms", nargs=-1)
@click.pass_context
def cli_say(ctx, output, terms):
    '''
    Say terms.
    '''
    m = ctx.obj
    
    text = ' '.join(terms)
    tmpfile = m.tts(text)
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
@click.argument("terms", nargs=-1)
@click.pass_context
def cli_read(ctx, output, terms):
    '''
    Provide reading for a phrase.
    '''
    m = ctx.obj

    reading = m.read(terms)
    if not output:
        print(reading)
        return
    Path(output).write_text(reading)

@cli.command("split")
@click.option("-o","--output", default=None, type=Path,
              help="Output to file, else stdout")
@click.argument("terms", nargs=-1)
@click.pass_context
def cli_split(ctx, output, terms):
    '''
    Split a phrase into words.
    '''
    m = ctx.obj

    words = ' '.join(m.split(' '.join(terms)))    
    if not output:
        print(words)
        return
    Path(output).write_text(words)

@cli.command("furigana")
@click.option("-o","--output", default=None, type=Path,
              help="Output to file, else stdout")
@click.argument("terms", nargs=-1)
@click.pass_context
def cli_furigana(ctx, output, terms):
    '''
    Split a phrase into words and append furigana to kanji.
    '''
    m = ctx.obj

    words = m.split(' '.join(terms))
    furi = ' '.join(m.furigana(words))
    if not output:
        print(furi)
        return
    Path(output).write_text(furi)


# fixme: make a generic command to run an arbitrary tool comand.
# @cli.command("kakasi")
# @click.option("-o","--output", default=None, type=Path,
#               help="Output to file, else stdout")
# @click.argument("terms", nargs=-1)
# @click.pass_context
# def cli_kakasi(ctx, output, terms):
#     '''
#     Run kakasi
#     '''
#     m = ctx.obj

#     got = m.kakasi(terms)
#     print(got)



@cli.command("dictionary")
@click.argument("terms", nargs=-1)
@click.pass_context
def cli_dictionary(ctx, terms):
    '''
    Show the dictionary lookup of the terms.
    '''
    m = ctx.obj

    text = ' '.join(terms)
    got = m.dictionary(text)        # fixme: throws if no dict entry
    print(got)


@cli.command("translate")
@click.argument("terms", nargs=-1)
@click.pass_context
def cli_translate(ctx, terms):
    '''
    Show the simple translation of the terms.
    '''
    m = ctx.obj

    text = ' '.join(terms)
    got = m.translate(text)
    print(got)


@cli.command("ui")
@click.argument("terms", nargs=-1)
@click.pass_context
def cli_ui(ctx, terms):
    '''
    Use user-interactive workflow.

    This combines displaying reading and translation and saying and optionally
    re-saying and saving to anki as governed by user interacting with a UI.
    '''
    m = ctx.obj

    text = ' '.join(terms)
    definition = m.dictionary(text)
    reading = m.read(text)
    saying = m.tts(text)
    m.play(saying)

    def callback(line):
        if line == "say":
            m.play(saying)
            return
        if line == "anki":
            print("saving to anki not yet supported")
            return
        raise RuntimeError(f'bad code logic, callback should not get: "{line}"')


    lines = [f'term: {text}']
    if reading != text:
        lines.append(f'reading: {reading}')
    lines.append(definition)
    uitext = '\n'.join(lines)
    buttons = {
        "say": callback,
        "anki": callback,
        "done": 0
    }

    m.dialog(uitext, title=text, buttons=buttons)
    


if __name__ == '__main__':
    cli()
