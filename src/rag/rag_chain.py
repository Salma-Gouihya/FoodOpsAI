
from src.rag.vector_store import search_documents
from src.generation.gemini_client import generate_text


def answer_question(question: str, n_results: int = 3) -> str:
    """
    Répond à une question en utilisant les documents
    retrouvés dans ChromaDB.
    """

    if not question.strip():
        return "Veuillez saisir une question."

    # 1. Recherche des passages pertinents
    results = search_documents(question, n_results)

    if not results["documents"] or not results["documents"][0]:
        return "Je n'ai trouvé aucun document pertinent pour répondre."

    # 2. Construction du contexte et des sources
    context_parts = []
    sources = []

    for document, metadata in zip(
        results["documents"][0],
        results["metadatas"][0]
    ):
        source = metadata["source"]
        page = metadata["page"]

        context_parts.append(
            f"Source : {source}, page : {page}\n"
            f"Contenu : {document}"
        )

        reference = f"{source}, page {page}"

        if reference not in sources:
            sources.append(reference)

    context = "\n\n".join(context_parts)

    # 3. Construction du prompt
    prompt = f"""
Tu es FoodOps AI, un assistant intelligent spécialisé
dans la gestion des opérations de restauration.

Réponds à la question en utilisant UNIQUEMENT
les informations présentes dans le contexte documentaire.

QUESTION :
{question}

CONTEXTE DOCUMENTAIRE :
{context}

CONSIGNES :
1. Réponds clairement et en français.
2. N'invente aucune information.
3. Si le contexte ne contient pas la réponse,
   indique clairement que tu ne disposes pas
   de cette information.
4. Ne présente pas une supposition comme un fait.
5. Ne donne aucune garantie concernant la sécurité
   ou la fraîcheur des aliments.
6. Cite les sources utilisées dans ta réponse.
7. Ne prétends jamais avoir consulté des documents
   qui ne figurent pas dans le contexte.

RÉPONSE :
"""

    # 4. Génération avec Gemini
    response = generate_text(prompt)

    # 5. Ajout des références documentaires
    source_text = "\n".join(
        f"- {source}" for source in sources
    )

    return (
        f"{response}\n\n"
        f"Sources documentaires :\n{source_text}"
    )


if __name__ == "__main__":

    print("\n===== FOODOPS AI : ASSISTANT DOCUMENTAIRE =====")

    question = (
       "Quel est le prix du kilogramme de saumon ?"
    )

    print("\nQuestion :", question)

    try:
        response = answer_question(question)
        print("\nRéponse de FoodOps AI :\n")
        print(response)

    except Exception as error:
        print(f"\nErreur : {error}")
