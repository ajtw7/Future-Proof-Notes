from datetime import datetime
from note import Note
from search import Search_notes
from pathlib import Path
from rich import print
from collections import Counter
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
    tags = typer.prompt("Tags (comma separated)")
    note.tags = tags.split(",") if tags else []
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


@app.command()
def search(query:str):
    """Search for notes containing the query string."""
    results = Search_notes(query)
    if not results:
        typer.echo("🔎 No matches found.")
    else:
        typer.echo("🔎 Search Results")
        for file_name, title in results: 
            print(f"file_name: {file_name}, [red]title: {title}[/red]")  # Use red color for output


@app.command()
def stats():
    """Display statistics about all notes."""            
    # Declare the notes directory
    notes_dir = Path("notes")
    # declare total notes count
    total_notes = 0
    # decalare total tags count
    tag_counter = Counter()
    # declare total length of all notes
    total_length = 0

    # load through all notes in the notes directory
    for note_file in notes_dir.glob("*.note"):
        # for each note, read its content
        with open(note_file, "r", encoding="utf-8") as f:
            content = f.read()
        # split the content on '---' to separate header and body
            parts = content.split("---")
                # if the split parts (header, body) are less than 3, continue to next file
            if len(parts) < 3:
                continue

            # assign header from parts [1]
            header = parts[1]

            # load the metadata from the header
            metadata = yaml.safe_load(header)

            # assign body from parts [2]
            body = parts[2].strip()

            # increment the total notes count
            total_notes += 1

            # update the total length of all notes
            total_length += len(body.split())

            # update the total tags count
            tag_counter.update(metadata.get('tags', []))

    # print the total notes count
    typer.echo(f"Total Notes: {total_notes}\n")
    # print the average length of all notes
    typer.echo(f"Avg Length of Notes: {total_length // total_notes if total_notes else 0} words\n")
    # print the total tags count using for loop
    typer.echo("Total Tags:")
    for tag, count in tag_counter.most_common(5):
        # print the tag and its count
        typer.echo(f" — {tag}: {count} occurrences")


if __name__ == "__main__":
    app()