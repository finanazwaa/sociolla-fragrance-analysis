import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
reviews_path = ROOT / "data" / "reviews.json"
output_path = ROOT / "data" / "reviews.csv"

if not reviews_path.exists():
    raise FileNotFoundError(f"Reviews file not found: {reviews_path}")

with reviews_path.open("r", encoding="utf-8") as handle:
    reviews = json.load(handle)

rows = []

for review in reviews:
    rows.append({
        "review_id": review.get("_id"),
        "product_id": review.get("product_id"),
        "review_text": review.get("message", ""),
        "rating": review.get("star"),
        "review_date": review.get("created_at")
    })

df = pd.DataFrame(rows)
df.to_csv(output_path, index=False, encoding="utf-8-sig")

print(df.head())
print(f"\nSaved {len(df)} reviews to {output_path}.")