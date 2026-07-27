import requests

url = "https://catalog-api2.sociolla.com/v3/brands/distinct/products"

params = {
    "filter": '{"categories.slug":"145-fragrance"}',
    "limit": 50,
    "skip": 50
}

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Referer": "https://www.sociolla.com/",
    "Origin": "https://www.sociolla.com"
}

response = requests.get(
    url,
    params=params,
    headers=headers
)

print(response.status_code)

data = response.json()["data"]

print(f"Total brands: {len(data)}\n")

for brand in data:
    print(
        f"{brand['name']} | "
        f"slug={brand['slug']} | "
        f"products={brand['total_products']}"
    )

print("Returned:", len(data))