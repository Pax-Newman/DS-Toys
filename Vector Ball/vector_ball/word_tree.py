from dataclasses import dataclass
from scipy.spatial import KDTree

import sentence_transformers as st
import pickle


@dataclass
class Option:
    word: str
    distance: float


class WordTree:
    def __init__(self, model: str, words: list[str]) -> None:
        self.model_name = model
        self.model = st.SentenceTransformer(model)
        self.words = words
        self.tree = KDTree(self.model.encode(words, show_progress_bar=True))

    def query(self, word: str, k=5) -> list[Option]:
        word_embedding = self.model.encode(word)

        dist, ind = self.tree.query(word_embedding, k=k)
        words = [self.words[i] for i in ind]

        options = [Option(word, dist) for word, dist in zip(words, dist)]

        return options

    def to_pickle(self, path: str) -> None:
        self.model = None
        with open(path, "wb") as f:
            pickle.dump(self, f)


def read_pickle(path: str) -> WordTree:
    with open(path, "rb") as f:
        obj = pickle.load(f)
    if not isinstance(obj, WordTree):
        raise TypeError("Pickled file is not a WordTree")

    obj.model = st.SentenceTransformer(obj.model_name)

    return obj


def from_txt(path: str, model: str) -> WordTree:
    with open(path, "r") as f:
        words = f.read().splitlines()
    return WordTree(model, words)
