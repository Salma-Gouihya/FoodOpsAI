from src.rag.document_loader import load_pdf_documents

if __name__ == "__main__":
    documents = load_pdf_documents()

    print(f"\nTotal des pages extraites : {len(documents)}")

    for doc in documents:
        print("\n==============================")
        print("Document :", doc["metadata"]["source"])
        print("Page :", doc["metadata"]["page"])
        print("Catégorie :", doc["metadata"]["category"])
        print("Contenu :", doc["content"][:300])