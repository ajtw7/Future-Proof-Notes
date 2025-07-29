import typer
app = typer.Typer()

@app.command()
def hello(name: str):
    typer.echo(f"Hello {name}")

@app.command()
def create():
    typer.echo("Creating a new note...")

@app.command()
def list():
    typer.echo("Listing notes...")

@app.command()
def read(note_id: int):
    typer.echo("Reading a note...")


if __name__ == "__main__":
    app()