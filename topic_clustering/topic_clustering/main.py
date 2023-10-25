from typing import Annotated
from pathlib import Path

import typer
import pandas as pd
import sentence_transformers as st

from .clustering import make_embeddings, by_topic_distance, make_topic_prototype
from .utils import parse_topic_arg, validate_topic_arg, validate_topic_objs


app = typer.Typer()


# --- Subcommands ---


@app.command()
def topic_distance(
    data: Annotated[Path, typer.Argument(help="Path to data", exists=True)],
    column: Annotated[str, typer.Argument(help="Column name for text data")],
    model: Annotated[str, typer.Argument(help="Sentence Transformer model name")],
    outfile: Annotated[Path, typer.Argument(help="Path to output file")],
    topic: Annotated[list[str], typer.Option(help="List of topic names and keywords")],
    min_docs: Annotated[
        int, typer.Option(help="Minimum number of documents to create topic embedding")
    ] = 5,
    max_docs: Annotated[
        int, typer.Option(help="Maximum number of documents to create topic embedding")
    ] = 20,
    sim: Annotated[
        float,
        typer.Option(
            help="Minimum similarity threshold for adding a document to a topic embedding"
        ),
    ] = 0.5,
):
    validate_topic_arg(topic)

    # Load model
    st_model = st.SentenceTransformer(model)

    # Load data
    documents = pd.read_csv(data)[column]
    doc_embeddings = make_embeddings(st_model, documents)

    # Build topic vectors
    topics = parse_topic_arg(topic)

    topics = [
        make_topic_prototype(
            st_model,
            t,
            doc_embeddings,
            min_docs,
            max_docs,
            sim,
        )
        for t in topics
    ]

    validate_topic_objs(topics)

    # Classify remaining documents (by distance to root topic vectors)
    classes = by_topic_distance(topics, doc_embeddings)

    documents["class"] = classes

    documents.to_csv(outfile, index=False)


# --- Run App ---

if __name__ == "__main__":
    app()
