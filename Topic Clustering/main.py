from typing import Annotated, Tuple
from pathlib import Path
import typer



app = typer.Typer()


# --- Subcommands ---

@app.command()
def topic_distance(
        data: Annotated[Path, typer.Argument(help="Path to data", exists=True)],
        column: Annotated[str, typer.Argument(help="Column name for text data")],
        model: Annotated[str, typer.Argument(help="Sentence Transformer model name")],
        topics: Annotated[list[str], typer.Option(help="List of topic names and keywords")],
        min_docs: Annotated[int, typer.Option(help="Minimum number of documents to create topic embedding")] = 5,
        max_docs: Annotated[int, typer.Option(help="Maximum number of documents to create topic embedding")] = 20,
        sim: Annotated[float, typer.Option(help="Minimum similarity threshold for adding a document to a topic embedding")] = 0.5,
        ):
    print("Nearest")

    # Load data
    # Load model

    # Build topic vectors

    # Classify remaining documents (by distance to root topic vectors)

@app.command()
def nearest_neighbor():
    print("Nearest Neighbor")

    # Load data
    # Load model

    # Build topic vectors

    # Classify remaining documents (by distance to root topic vectors)

# --- Run App ---

if __name__ == "__main__":
    app()
