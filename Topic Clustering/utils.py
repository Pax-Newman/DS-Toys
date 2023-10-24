from clustering import Topic, make_topic_prototype


def validate_topic_arg(topics: list[str]) -> None:
    """
    Validate topic argument. Quits if invalid.
    """
    # Check for missing topics
    if len(topics) == 0:
        print("No topics specified.")
        quit()

    # Check for missing colon
    if not all([":" in topic for topic in topics]):
        print("Topics must be specified as '--topic topic_name:keyword1,keyword2,...'")
        quit()

    # Check for too many colons
    if not all([len(topic.split(":")) == 2 for topic in topics]):
        print("Topics must be specified as '--topic topic_name:keyword1,keyword2,...'")
        quit()


def validate_topic_objs(topics: list[Topic]):
    """
    Validate topic objects. Quits if invalid.
    """

    # Check for missing keywords
    if not all([len(topic.keywords) > 0 for topic in topics]):
        print("Topics must have at least one keyword.")
        quit()

    # Check for duplicate topic names
    if len(set([topic.name for topic in topics])) != len(topics):
        print("Topics must have unique names.")
        quit()


def parse_topic_arg(
    model, topics, doc_embeddings, min_docs, max_docs, sim
) -> list[Topic]:
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
