from datetime import datetime
from note import Note
from pathlib import Path
import yaml
import typer
import subprocess
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
    filename = f"{note.note_id}.note"
    filepath = Path("notes") / filename
    with open(filepath, "w", encoding="utf-8") as f: #  Ensure the file is opened in write mode
        f.write(note.to_yaml()) # Write the YAML representation of the note
    typer.echo(f"Note saved to {filepath}")
    typer.echo(f"Note ID: {note.note_id}")

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
                metadata = yaml.safe_load(header)
                typer.echo(f"{note_file.name}: {metadata['title']} (Created: {metadata.get('created')}) [{metadata.get('note_id')}]")
            except Exception as e:
                typer.echo(f"{note_file.name}: Error reading metadata - {e}")
    

@app.command()
def read(note_id: str):
    # define the file path based on note_id
    file_path = Path("notes") / f"{note_id}.note"
    # if the filepath does not exist, raise an error
    if not file_path.exists():
        typer.echo("Note not found")
        raise typer.Exit(code=1)
    # open the file and read its content
    with open(file_path, "r", encoding="utf-8") as f:
    # define the main vars of the fn: parts and content
        content = f.read()
        parts = content.split("---")
        # if parts doesn't start with '---', AND have 3 parts, raise an error
        if len(parts) < 3:
                typer.echo("Invalid note format")
                raise typer.Exit(code=1)
    # Define all parts [header, metadata, body]
        header = parts[1]
        metadata = yaml.safe_load(header) if header else {}
        body = parts[2].strip()
    #Print Metadata and body
        typer.echo("🗒️ Metadata:")
        # For loop through metadata based on key:value pairs (metadata.items())
        for key, value in metadata.items():
            typer.echo(f"{key}: {value}")
        typer.echo("\n📝 Content:")
        typer.echo(body)

@app.command()
def edit(note_id: str):
    file_path = Path("notes") / f"{note_id}.note"
    if not file_path.exists():
        typer.echo("Note not found")
        raise typer.Exit(code=1)
    subprocess.call([os.environ.get("EDITOR", 'nano'), str(file_path)]) # Open the file in the default editor
    # update modified timestamp
    with open(file_path, "r+", encoding="utf-8") as f:
        content = f.read()
        parts = content.split("---")
        if len(parts) < 3:
            typer.echo("invalid note format")
            raise typer.Exit(code=1)
        header = parts[1]
        body = parts[2].lstrip('\n')

        metadata = yaml.safe_load(header)
        metadata['modified'] = datetime.utcnow().isoformat() + "Z"  # Update modified timestamp

        # set new variables for metadata, content, and body
        new_content = f"---\n{yaml.dump(metadata)}---\n{body}"
        f.seek(0)
        f.write(new_content)
        f.truncate()
        typer.echo(f"{metadata['title']} updated successfully.")


@app.command()
def delete(note_id:str):
    # define the file path based on note_id
    file_path = Path("notes") / f"{note_id}.note"
    
    # define the trash path
    trash_path = Path("trash") / f"{note_id}.note"

    # if the file path doesn't exist, raise an error
    if not file_path.exists():
        typer.echo("Note not found")
        raise typer.Exit(code=1)
    
    # rename the file_path to the trash path
    file_path.rename(trash_path)
    
    # Print success message
    typer.echo(f"Note {note_id} moved to trash.")




if __name__ == "__main__":
    app()