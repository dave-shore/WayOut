from fastapi import FastAPI
import chromadb
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
from chromadb.utils import embedding_functions
from config import *

language = "it"
COUNTER = 0

app = FastAPI()
CHROMA_CLIENT = chromadb.PersistentClient(
    path="wayout",
    settings=Settings(),
    tenant=DEFAULT_TENANT,
    database=DEFAULT_DATABASE,
)

sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=MODELS[language])
collection = CHROMA_CLIENT.create_collection("wayout", embedding_function=sentence_transformer_ef)

# Write page
@app.get("/write/{kind}/get")
def suggest(kind: str, text: str):

    results = collection.query(
        query_texts = text,
        n_results = 3,
        where = {"kind": kind}
    )

    return results

@app.post("/write/{kind}/post")
def write(kind: str, text: str):

    collection.add(
        ids = [COUNTER],
        documents = [text],
        metadatas = [{"kind": kind}]
    )

    COUNTER += 1

    