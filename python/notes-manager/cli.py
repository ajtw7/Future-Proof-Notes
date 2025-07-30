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
    notes_dir = Path("notes") # declaring notes path
    for note_file in notes_dir.glob("*.note"):
        with open(note_file, "r", encoding="utf-8") as f:
            content = f.read()
            # Skip empty files
            if not content.strip():
                continue
            # Split on '---' and check if we have at least 2 '---' blocks
            parts = content.split("---")
            if len(parts) < 3: # all notes should start with '---' and end with '---'
                typer.echo(f"{note_file.name}: Invalid note format") 
                continue
            header = parts[1]
            try:
                import yaml
                metadata = yaml.safe_load(header)
                typer.echo(f"{note_file.name}: {metadata['title']} (Created: {metadata['created']})")
            except Exception as e:
                typer.echo(f"{note_file.name}: Error reading metadata - {e}")
    

@app.command()
def read(note_id: int):
    # define the file path based on note_id
    # if the filepath does not exist, raise an error
    # open the file and read its content
    # define the main vars of the fn: parts and content
        # if parts doesn't start with '---', AND have 3 parts, raise an error
    # Define all parts [header, metadata, body]
    #Print Metadata and body
        # For loop through metadata based on key:value pairs (metadata.items())

    typer.echo("Reading a note...")


if __name__ == "__main__":
    app()