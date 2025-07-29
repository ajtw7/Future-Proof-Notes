from note import Note
from pathlib import Path
import typer
import os

app = typer.Typer()

@app.command()
def hello(name: str):
    typer.echo(f"Hello {name}")

@app.command()
def create():
    title = typer.prompt("Title")
    content = typer.prompt("Content")
    note = Note(title=title, content=content)
    filename = f"{title.replace(' ', '_')}_{note.created}.note"
    filepath = Path("notes") / filename
    with open(filepath, "w", encoding="utf-8") as f: #  Ensure the file is opened in write mode
        f.write(note.to_yaml()) # Write the YAML representation of the note
    typer.echo(f"Note saved to {filepath}")

@app.command()
def list():
    typer.echo("Listing notes...")

@app.command()
def read(note_id: int):
    typer.echo("Reading a note...")


if __name__ == "__main__":
    app()