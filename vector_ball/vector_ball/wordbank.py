import pandas as pd
import sentence_transformers as st
from pycozo.client import Client

from os import path


class WordBank:
    def __init__(self, db_path: str, model: str | None = None) -> None:
        # Check that the directory exists
        if not path.exists(path.dirname(db_path)):
            raise FileNotFoundError(f"Directory {path.dirname(db_path)} does not exist")

        # Create a new database if one doesn't exist at the given path
        if not path.exists(db_path):
            if model is None:
                raise ValueError(
                    "Must provide a model name when creating a new database"
                )

            self.model = st.SentenceTransformer(model)
            emb_size = self.model.encode("test").shape[0]

            self.db = Client("sqlite", db_path)

            # Create wordbank relation
            self.db.run(
                f":create wordbank {{ word: String => embedding: <F32; {emb_size}> }}"
            )

            # Create vector index
            self.db.run(
                f"::hnsw create wordbank:semantic{{ fields: [embedding], dim: {emb_size}, ef: 16, m: 32, distance: L2 }}"
            )

        # Load existing database
        else:
            self.db = Client("sqlite", db_path)

            # FIXME: We should check if the model matches that of the db
            self.model = st.SentenceTransformer(model)

    def put(self, words: list[str]) -> None:
        embeddings = self.model.encode(words)
        embeddings = [e.tolist() for e in embeddings]

        self.db.put("wordbank", pd.DataFrame({"word": words, "embedding": embeddings}))

    def query(self, word: str, k: int = 5) -> list[tuple[str, float]]:
        res: pd.DataFrame = self.db.run(
            f"""
            ?[word, dist] :=
                *wordbank{{word: "{word}", embedding: e}},
                ~wordbank:semantic{{word | query: e, bind_distance: dist, k: {k}, ef: 50}}
            :order dist
            :limit {k}
            """
        )
        out = [(word, dist) for word, dist in zip(res["word"], res["dist"])]
        return out


def from_txt(txt_path: str, model: str) -> WordBank:
    with open(txt_path, "r") as f:
        words = f.read().splitlines()

    dir_path, f_name = path.split(txt_path)
    f_name, _ = path.splitext(f_name)

    db_path = path.join(dir_path, f"{f_name}.db")

    wb = WordBank(db_path, model)
    wb.put(words)

    return wb

