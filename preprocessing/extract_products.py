import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
products_path = ROOT / "data" / "products.json"
output_path = ROOT / "data" / "products.csv"

with products_path.open("r", encoding="utf-8") as handle:
    products = json.load(handle)

rows = []

for product in products:
    rows.append({
        "product_id": product["id"],
        "product_name": product["name"],
        "brand_id": product["brand"]["id"],
        "price": product["default_combination"]["price"],
        "avg_rating": product["review_stats"]["average_rating"],
        "description": product.get("description", "")
    })

df = pd.DataFrame(rows)
df.to_csv(output_path, index=False, encoding="utf-8-sig")

print(df.head())
print(f"\nSaved {len(df)} products to {output_path}.")