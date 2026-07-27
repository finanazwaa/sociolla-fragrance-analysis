import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scraper.get_products import get_all_products
from scraper.get_reviews import get_reviews


def main():
    output_path = ROOT / "data" / "reviews.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    all_reviews = []

    try:
        products = get_all_products()
    except Exception as exc:
        print(f"Could not fetch products from API: {exc}")
        products = []

    for product in products:
        try:
            reviews = get_reviews(product["id"])
        except Exception as exc:
            print(f"Skipping {product['id']}: {exc}")
            continue

        all_reviews.extend(reviews)

    with output_path.open("w", enacoding="utf-8") as handle:
        json.dump(all_reviews, handle, ensure_ascii=False, indent=2)

    print(f"Saved {len(all_reviews)} reviews to {output_path}")


if __name__ == "__main__":
    main()