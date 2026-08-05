import json
from .get_products import get_all_products

products = get_all_products()

with open("data/products.json", "w", encoding="utf-8") as f:
    json.dump(products, f, ensure_ascii=False, indent=4)

print(f"Saved {len(products)} products!")