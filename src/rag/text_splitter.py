
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.rag.document_loader import load_pdf_documents


def split_documents(documents):
    """Découpe les pages PDF en petits morceaux de texte."""

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
        separators=["\n\n", "\n", ". ", " ", ""],
        add_start_index=True
    )

    chunks = []

    for document in documents:
        parts = splitter.split_text(document["content"])

        for index, part in enumerate(parts):
            chunks.append({
                "content": part,
                "metadata": {
                    **document["metadata"],
                    "chunk_index": index
                }
            })

    return chunks


if __name__ == "__main__":
    documents = load_pdf_documents()
    chunks = split_documents(documents)

    print(f"\nNombre total de chunks : {len(chunks)}")

    for chunk in chunks:
        print("\n==============================")
        print("Source :", chunk["metadata"]["source"])
        print("Page :", chunk["metadata"]["page"])
        print("Chunk :", chunk["metadata"]["chunk_index"])
        print("Texte :", chunk["content"][:300])
