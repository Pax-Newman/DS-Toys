from dataclasses import dataclass
from typing import Iterable

import numpy as np
import sentence_transformers as st

import pandas as pd


@dataclass
class Topic:
    name: str
    keywords: list[str]
    doc_indices: list[int] | None = None
    embedding: np.ndarray | None = None


def cos_sim(a: np.ndarray, b: np.ndarray) -> float:
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def make_embeddings(
    model: st.SentenceTransformer, documents: Iterable[str]
) -> np.ndarray:
    if not isinstance(documents, list):
        documents = list(documents)

    embeddings = model.encode(documents)

    return embeddings


def make_topic_prototype(
    model: st.SentenceTransformer,
    topic: Topic,
    doc_embeddings: np.ndarray,
    min_docs: int = 5,
    max_docs: int = 20,
    sim_thresh: float = 0.5,
) -> Topic:
    # Generate keyword embeddings
    kw_embeddings = make_embeddings(model, topic.keywords)

    # Make keyword prototype
    kw_proto = kw_embeddings.mean(axis=0)

    # Find max_docs closest documents to keyword prototype
    doc_similarities = np.dot(kw_proto, doc_embeddings.T)

    candidate_doc_indices = np.argsort(doc_similarities)[::-1][:max_docs]
    candidate_doc_sims = doc_embeddings[candidate_doc_indices]

    # Ensure that the number of candidates is within min and max specifications
    if len(np.where(candidate_doc_sims >= sim_thresh)) <= min_docs:
        topic.doc_indices = list(candidate_doc_indices[:min_docs])
    else:
        topic.doc_indices = []
        for sim, ind in zip(
            doc_similarities[candidate_doc_indices], candidate_doc_indices
        ):
            if sim < sim_thresh:
                break
            topic.doc_indices.append(ind)

    # Make topic prototype with document embeddings
    topic.embedding = doc_embeddings[topic.doc_indices].mean(axis=0)

    return topic


def by_topic_distance(
    topics: list[Topic],
    doc_embeddings: np.ndarray,
) -> list[str]:
    # PERF: This could be sped up by using a KDTree or vectorized operations
    def classify(doc: np.ndarray) -> str:
        return max(
            topics,
            key=lambda t: cos_sim(doc, t.embedding),
        ).name

    doc_classes = [classify(doc) for doc in doc_embeddings]

    return doc_classes


def by_nearest_neighbor():
    ...
