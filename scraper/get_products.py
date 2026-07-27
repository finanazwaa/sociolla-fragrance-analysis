import requests
import json
import time

URL = "https://catalog-api3.sociolla.com/search"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Referer": "https://www.sociolla.com/",
    "Origin": "https://www.sociolla.com"
}

FILTER = {
    "categories.id": "5d3d50276b24d0159951681d",   # Fragrance
    "classification": {
        "$nin": [
            "gwp_non_sellable",
            "bundle_non_sellable",
            "testers"
        ]
    }
}


def get_all_products():

    all_products = []

    limit = 50
    skip = 0

    while True:

        print(f"Fetching {skip} ...")

        response = requests.get(
            URL,
            params={
                "filter": json.dumps(FILTER),
                "limit": limit,
                "skip": skip,
                "sort": "-six_month_total_orders"
            },
            headers=HEADERS
        )

        response.raise_for_status()

        products = response.json()["data"]

        print("Returned:", len(products))

        if len(products) == 0:
            break

        all_products.extend(products)

        skip += limit

        time.sleep(0.3)

    return all_products


if __name__ == "__main__":

    products = get_all_products()

    print("\n==============================")
    print("TOTAL PRODUCTS:", len(products))
    print("==============================\n")

    for p in products:
        print(
            f"{p['id']} | "
            f"{p['brand']['name']} | "
            f"{p['name']}"
        )