
import pandas as pd
from pathlib import Path
from datetime import date, timedelta


BASE_DIR = Path(__file__).resolve().parents[2]
INVENTORY_FILE = BASE_DIR / "data" / "inventory" / "inventory.csv"


def load_inventory():
    """Charge les données du stock depuis le fichier CSV."""
    if not INVENTORY_FILE.exists():
        raise FileNotFoundError("Fichier inventory.csv introuvable")

    df = pd.read_csv(INVENTORY_FILE)

    required_columns = {
        "product_id",
        "product_name",
        "category",
        "quantity",
        "unit",
        "min_quantity",
        "expiry_date"
    }

    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(f"Colonnes manquantes : {missing}")

    df["expiry_date"] = pd.to_datetime(
        df["expiry_date"], errors="coerce"
    )

    return df


def get_low_stock():
    """Retourne les produits sous leur seuil minimum."""
    df = load_inventory()

    low_stock = df[df["quantity"] < df["min_quantity"]]

    return low_stock


def get_expiring_products(days=3):
    """Retourne les produits qui expirent dans les prochains jours."""
    df = load_inventory()

    today = pd.Timestamp(date.today())
    limit_date = today + timedelta(days=days)

    expiring = df[
        (df["expiry_date"] >= today) &
        (df["expiry_date"] <= limit_date)
    ]

    return expiring


def get_inventory_summary():
    """Prépare un résumé global du stock."""
    df = load_inventory()

    return {
        "total_products": len(df),
        "low_stock_count": len(
            df[df["quantity"] < df["min_quantity"]]
        ),
        "total_categories": df["category"].nunique()
    }
