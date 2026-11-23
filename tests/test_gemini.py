from src.generation.gemini_client import generate_text

if __name__ == "__main__":
    response = generate_text(
        "Présente FoodOps AI en deux phrases."
    )
    print("\nRéponse de Gemini :")
    print(response)
