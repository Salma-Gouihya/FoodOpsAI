
from pathlib import Path
from src.rag.document_loader import load_pdf_documents
import chromadb
from sentence_transformers import SentenceTransformer

from src.rag.text_splitter import split_documents

BASE_DIR = Path(__file__).resolve().parents[2]
CHROMA_DIR = BASE_DIR / "data" / "chroma_db"

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
COLLECTION_NAME = "foodops_documents"

# Initialisation du modèle et de ChromaDB
embedding_model = SentenceTransformer(MODEL_NAME)

chroma_client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = chroma_client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"}
)



def index_documents():
    """Transforme les chunks en embeddings et les stocke."""

    documents = load_pdf_documents()
    chunks = split_documents(documents)

    if not chunks:
        print("Aucun chunk à indexer.")
        return

    ids = []
    texts = []
    metadatas = []

    for chunk in chunks:
        metadata = chunk["metadata"]

        chunk_id = (
            f"{metadata['source']}_"
            f"{metadata['page']}_"
            f"{metadata['chunk_index']}"
        )

        ids.append(chunk_id)
        texts.append(chunk["content"])
        metadatas.append(metadata)

    embeddings = embedding_model.encode(
        texts,
        normalize_embeddings=True
    ).tolist()

    collection.upsert(
        ids=ids,
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings
    )

    print(f"{len(ids)} chunks indexés avec succès.")
    print(f"Nombre total de documents dans ChromaDB : {collection.count()}")


def search_documents(query: str, n_results: int = 3):
    """Recherche les passages les plus proches d'une question."""

    query_embedding = embedding_model.encode(
        query,
        normalize_embeddings=True
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(n_results, collection.count())
    )

    return results


if __name__ == "__main__":
    index_documents()

    print("\n===== TEST DE RECHERCHE =====")

    question = "Quels ingrédients faut-il pour préparer une salade de poulet ?"

    results = search_documents(question)

    for document, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        print("\n------------------------------")
        print("Source :", metadata["source"])
        print("Page :", metadata["page"])
        print("Distance :", round(distance, 4))
        print("Contenu :", document[:400])
