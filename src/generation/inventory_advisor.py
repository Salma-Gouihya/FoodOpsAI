
import json

from src.inventory.inventory_manager import (
    get_inventory_summary,
    get_low_stock,
    get_expiring_products
)
from src.generation.gemini_client import generate_text


def generate_inventory_report():

    summary = get_inventory_summary()

    low_stock = get_low_stock()
    expiring = get_expiring_products(days=3)

    low_stock_data = low_stock.to_dict(orient="records")
    expiring_data = expiring.to_dict(orient="records")

    # Convertir les dates pour le format JSON
    for product in low_stock_data + expiring_data:
        if product["expiry_date"] is not None:
            product["expiry_date"] = str(product["expiry_date"])

    inventory_context = {
        "summary": summary,
        "low_stock_products": low_stock_data,
        "expiring_products": expiring_data
    }

    prompt = f"""
    Tu es un assistant intelligent spécialisé dans
    la gestion des stocks de restaurants.

    Analyse les informations suivantes :

    {json.dumps(inventory_context, ensure_ascii=False, indent=2)}

    Consignes :
    1. Présente un résumé de la situation.
    2. Identifie les produits à réapprovisionner.
    3. Signale les produits proches de leur expiration.
    4. Propose des actions prioritaires pour limiter le gaspillage.
    5. Utilise uniquement les données fournies.
    6. Ne modifie aucune quantité et ne prétends pas
       avoir effectué une commande.
    7. Rédige une réponse claire et professionnelle en français.
    """

    return generate_text(prompt)
