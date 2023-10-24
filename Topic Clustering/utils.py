from clustering import Topic, make_topic_prototype


def parse_topic_arg(model, topics, doc_embeddings, min_docs, max_docs, sim) -> list[Topic]:
    topics = [
        Topic(
            topic_str.split(":")[0],
            topic_str.split(":")[1].split(","),
        )
        for topic_str in topics
    ]

    topics = [
        make_topic_prototype(
            model,
            topic,
            doc_embeddings,
            min_docs,
            max_docs,
            sim,
        )
        for topic in topics
    ]

    return topics

