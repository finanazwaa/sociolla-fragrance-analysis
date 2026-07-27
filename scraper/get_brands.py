import requests

URL = "https://catalog-api2.sociolla.com/v3/brands/distinct/products"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Referer": "https://www.sociolla.com/",
    "Origin": "https://www.sociolla.com"
}


def get_brands():
    session = requests.Session()
    session.trust_env = False

    response = session.get(
        URL,
        params={
            "filter": '{"categories.slug":"145-fragrance"}',
            "limit": 50,
            "skip": 0
        },
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    return response.json()["data"]


if __name__ == "__main__":

    brands = get_brands()

    for b in brands:
        print(
            b["_id"],
            b["name"],
            b["total_products"]
        )