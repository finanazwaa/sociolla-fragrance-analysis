import requests
import json
import time

from get_products import get_all_products

URL = "https://soco-api.sociolla.com/reviews"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Referer": "https://www.sociolla.com/",
    "Origin": "https://www.sociolla.com"
}


def get_reviews(product_id):

    reviews = []

    limit = 20
    skip = 0

    while True:

        response = requests.get(
            URL,
            params={
                "filter": json.dumps({
                    "is_published": True,
                    "elastic_search": True,
                    "product_id": product_id
                }),
                "sort": "most_relevant",
                "limit": limit,
                "skip": skip
            },
            headers=HEADERS
        )

        response.raise_for_status()

        result = response.json()

        data = result.get("data", [])

        if len(data) == 0:
            break

        reviews.extend(data)

        if len(data) < limit:
            break

        skip += limit
        time.sleep(0.2)

    return reviews


if __name__ == "__main__":

    products = get_all_products()

    all_reviews = []

    for product in products:

        pid = product["id"]

        print(f"Fetching reviews for {pid} - {product['name']}")

        reviews = get_reviews(pid)

        print(f"  {len(reviews)} reviews")

        all_reviews.extend(reviews)

        time.sleep(0.2)

    print("\n==========================")
    print("TOTAL REVIEWS:", len(all_reviews))
    print("==========================")

    # Simpan ke JSON
    with open("../data/reviews.json", "w", encoding="utf-8") as f:
        json.dump(all_reviews, f, ensure_ascii=False, indent=2)