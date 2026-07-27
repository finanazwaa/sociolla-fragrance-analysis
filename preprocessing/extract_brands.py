import json
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from scraper.get_brands import get_brands
except ModuleNotFoundError:
    get_brands = None

if get_brands is not None:
    try:
        brands = get_brands()
    except Exception as exc:
        print(f"API request failed, falling back to local data: {exc}")
        brands = None
else:
    brands = None

rows = []

if brands is not None:
    for b in brands:
        rows.append({
            "brand_id": b["_id"],
            "brand_name": b["name"]
        })
else:
    products_path = ROOT / "data" / "products.json"
    with products_path.open("r", encoding="utf-8") as handle:
        products = json.load(handle)

    seen = {}
    for product in products:
        brand = product.get("brand") or {}
        brand_id = brand.get("id")
        brand_name = brand.get("name")
        if brand_id and brand_id not in seen:
            seen[brand_id] = brand_name or ""
            rows.append({
                "brand_id": brand_id,
                "brand_name": brand_name
            })

df = pd.DataFrame(rows)

output_path = ROOT / "data" / "brands.csv"
df.to_csv(output_path, index=False, encoding="utf-8-sig")

print(df.head())
print(f"\nSaved {len(df)} brands to {output_path}.")