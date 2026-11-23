from src.generation.gemini_client import client

print("Modèles disponibles pour la génération :\n")

for model in client.models.list():
    actions = model.supported_actions or []
    if "generateContent" in actions:
        print(model.name)
