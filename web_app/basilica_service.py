import basilica
import os
from .env import load_dotenv

BASILICA_API_KEY = os.getnev("BASILICA_API_KEY", default="OOPS")

sentences = [
    "This is a sentence!",
    "This is a similar sentence!",
    "I dont' htink this sentence is very similar at all."
]

with basilica.Connection(BASILICA_API_KEY) as c:
    embeddings = list(c.embed_sentence(sentences))
