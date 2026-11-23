
from src.inventory.inventory_manager import (
    load_inventory,
    get_low_stock,
    get_expiring_products,
    get_inventory_summary
)

print("\n===== INVENTAIRE COMPLET =====")
print(load_inventory().to_string(index=False))

print("\n===== PRODUITS EN STOCK FAIBLE =====")
print(get_low_stock().to_string(index=False))

print("\n===== PRODUITS BIENTOT PERIMES =====")
print(get_expiring_products().to_string(index=False))

print("\n===== RESUME DU STOCK =====")
print(get_inventory_summary())
