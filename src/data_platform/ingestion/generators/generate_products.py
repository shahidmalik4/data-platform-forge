import uuid
import random
from datetime import datetime
from faker import Faker
import os

from data_platform.ingestion.utils.db_utils import fetch_table, is_first_run
from data_platform.ingestion.utils.corrupt_data import corrupt_list

fake = Faker()

NO_OF_PRODUCTS = 450
NO_NEW_PRODUCTS = 9

CATALOG = {
    "Electronics": {
        "Smartphones": ["iPhone 14", "Galaxy S23", "Pixel 7"],
        "Laptops": ["MacBook Air", "Dell XPS 13", "HP Spectre"],
        "Accessories": ["Wireless Mouse", "Bluetooth Headphones", "USB-C Hub"]
    },
    "Clothing": {
        "Men": ["T-Shirt", "Jeans", "Jacket"],
        "Women": ["Dress", "Top", "Skirt"]
    },
    "Home": {
        "Kitchen": ["Blender", "Microwave", "Toaster"],
        "Furniture": ["Sofa", "Dining Table", "Chair"]
    },
    "Books": {
        "Fiction": ["Mystery Novel", "Sci-Fi Book"],
        "Non-Fiction": ["Self Help Book", "Biography"]
    }
}

BRANDS = {
    "Electronics": ["Apple", "Samsung", "Sony", "Dell"],
    "Clothing": ["Nike", "Adidas", "Zara", "H&M"],
    "Home": ["IKEA", "Philips", "LG"],
    "Books": ["Penguin", "HarperCollins", "O'Reilly"]
}

PRICE_RANGES = {
    "Electronics": (100, 2000),
    "Clothing": (10, 200),
    "Home": (20, 1000),
    "Books": (5, 50)
}


# -------------------------------
# Safe price generation
# -------------------------------
def generate_price_and_cost(category):
    min_price, max_price = PRICE_RANGES[category]

    price = round(random.uniform(min_price, max_price), 2)

    margin = random.uniform(0.2, 0.6)
    cost = round(price * (1 - margin), 2)

    return price, cost


# -------------------------------
# Create product (SAFE)
# -------------------------------
def create_product():
    category = random.choice(list(CATALOG.keys()))
    subcategory = random.choice(list(CATALOG[category].keys()))
    base_product = random.choice(CATALOG[category][subcategory])
    brand = random.choice(BRANDS[category])

    price, cost = generate_price_and_cost(category)

    return {
        "product_id": str(uuid.uuid4()),
        "sku": f"{category[:3].upper()}-{random.randint(10000, 99999)}",
        "product_name": f"{brand} {base_product}",
        "category": category,
        "subcategory": subcategory,
        "brand": brand,
        "price": max(price, 0),
        "cost": max(cost, 0),
        "profit": round(price - cost, 2),
        "stock_quantity": max(0, random.randint(0, 500)),
        "rating": round(random.uniform(2.5, 5.0), 1),
        "is_active": random.choices([True, False], weights=[0.85, 0.15])[0],
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }


# -------------------------------
# Run generation
# -------------------------------
def run_product_generation():
    first_run = is_first_run("products")
    n = NO_OF_PRODUCTS if first_run else NO_NEW_PRODUCTS

    products = [create_product() for _ in range(n)]

    # ONLY apply corruption if enabled
    if os.getenv("DATA_MODE") == "chaos":
        products = corrupt_list(products, record_type="product")

    # ALWAYS enforce final safety ONLY in chaos mode
    if os.getenv("DATA_MODE") == "chaos":
        for p in products:
            p["price"] = max(0.01, abs(p.get("price", 0) or 0))
            p["cost"] = max(0.01, abs(p.get("cost", 0) or 0))

    return products