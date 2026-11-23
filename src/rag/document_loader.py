
from pathlib import Path
import pymupdf


BASE_DIR = Path(__file__).resolve().parents[2]
DOCUMENTS_DIR = BASE_DIR / "data" / "documents"


def load_pdf_documents():
    """Extrait le texte de tous les PDF du dossier documents."""

    documents = []

    pdf_files = list(DOCUMENTS_DIR.rglob("*.pdf"))

    if not pdf_files:
        print("Aucun document PDF trouvé.")
        return documents

    for pdf_path in pdf_files:
        try:
            pdf = pymupdf.open(pdf_path)

            for page_number, page in enumerate(pdf, start=1):
                text = page.get_text("text").strip()

                if text:
                    documents.append({
                        "content": text,
                        "metadata": {
                            "source": pdf_path.name,
                            "page": page_number,
                            "category": pdf_path.parent.name
                        }
                    })

            pdf.close()

        except Exception as error:
            print(f"Erreur avec {pdf_path.name} : {error}")

    return documents


if __name__ == "__main__":
    docs = load_pdf_documents()

    print(f"\nNombre de pages extraites : {len(docs)}")

    for doc in docs[:3]:
        print("\n------------------------------")
        print("Source :", doc["metadata"]["source"])
        print("Page :", doc["metadata"]["page"])
        print("Texte :", doc["content"][:500])
