from pathlib import Path
from typing import List, Dict

import faiss
import numpy as np

from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parent

KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"


print("Loading RAG embedding model...")

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def load_documents() -> List[str]:

    documents = []


    for file_path in KNOWLEDGE_BASE_DIR.glob("*.txt"):

        text = file_path.read_text(
            encoding="utf-8"
        ).strip()


        if text:

            documents.append(text)


    return documents


def build_vector_index():

    documents = load_documents()


    if not documents:

        raise ValueError(
            "No documents found in the knowledge base."
        )


    embeddings = embedding_model.encode(

        documents,

        convert_to_numpy=True

    )


    embeddings = embeddings.astype(

        "float32"

    )


    dimension = embeddings.shape[1]


    index = faiss.IndexFlatL2(

        dimension

    )


    index.add(

        embeddings

    )


    return index, documents


print("Building RAG vector index...")

index, documents = build_vector_index()

print(
    f"RAG loaded successfully. Documents: {len(documents)}"
)


def retrieve_relevant_context(

    query: str,

    top_k: int = 3

) -> List[Dict]:


    query_embedding = embedding_model.encode(

        [query],

        convert_to_numpy=True

    )


    query_embedding = query_embedding.astype(

        "float32"

    )


    distances, indices = index.search(

        query_embedding,

        min(top_k, len(documents))

    )


    results = []


    for distance, index_position in zip(

        distances[0],

        indices[0]

    ):


        results.append({

            "text": documents[index_position],

            "score": float(distance)

        })


    return results