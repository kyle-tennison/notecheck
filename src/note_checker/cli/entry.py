from pathlib import Path
from typer import Typer, Option
import typer
from loguru import logger
from note_checker.lib.checker import NoteChecker


app = typer.Typer(pretty_exceptions_enable=False)


@app.command()
def run(notes_root: Path = Option("~/obsidian/notes", help="The path to the notes root.")):
    """Run the note checking app"""
    logger.info("Starting note checker...")

    NoteChecker(notes_root).process()


