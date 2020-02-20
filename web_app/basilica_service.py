import os
from dotenv import load_dotenv
import basilica

load_dotenv()

BASILICA_API_KEY = os.getenv("BASILICA_API_KEY", default="OOPS")

connection = basilica.Connection(BASILICA_API_KEY)


def embed_tweets(tweets):
    """Return a list of basilica embeddings for a given list of tweets."""
    return list(connection.embed_sentences(tweets))

embeddings = list(connection.embed_sentences(sentences))
