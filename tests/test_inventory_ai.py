
from src.generation.inventory_advisor import generate_inventory_report


if __name__ == "__main__":
    print("\n===== FOODOPS AI : ANALYSE INTELLIGENTE DU STOCK =====\n")

    try:
        report = generate_inventory_report()
        print(report)

    except Exception as error:
        print(f"Erreur pendant l'analyse : {error}")
