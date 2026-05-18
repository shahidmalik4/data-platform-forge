import os
import random
import psycopg2
from dotenv import load_dotenv
from datetime import datetime, timezone


load_dotenv()


COUNTRY_CITY_MAP = {
    "United States": ["New York", "Los Angeles", "Chicago", "Houston", "San Francisco", "Seattle"],
    "United Kingdom": ["London", "Manchester", "Birmingham"],
    "Canada": ["Toronto", "Vancouver", "Montreal"],
    "Germany": ["Berlin", "Munich", "Hamburg"],
    "France": ["Paris", "Lyon", "Marseille"],
    "Australia": ["Sydney", "Melbourne", "Brisbane"],
    "Pakistan": ["Lahore", "Karachi", "Islamabad", "Skardu"],
    "Brazil": ["São Paulo", "Rio de Janeiro"],
    "Japan": ["Tokyo", "Osaka"],
    "China": ["Beijing", "Shanghai"],
    "UAE": ["Dubai", "Abu Dhabi"],
    "Italy": ["Rome", "Milan"],
    "Spain": ["Madrid", "Barcelona"],
    "Netherlands": ["Amsterdam", "Rotterdam"],
    "Saudi Arabia": ["Riyadh", "Jeddah", "Dammam"]
}

SEGMENTS = ["free", "pro", "enterprise"]

SEGMENT_UPDATE_PROB = {
    "free": 0.7,
    "pro": 0.5,
    "enterprise": 0.2
}


def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )


# CUSTOMER UPDATES
def update_customers(batch_size=50, update_count=10):
    conn = get_connection()
    cur = conn.cursor()

    # Fetch recent customers
    cur.execute("""
        SELECT customer_id, country, city, segment, engagement_score
        FROM raw.customers
        ORDER BY updated_at DESC NULLS LAST, customer_id DESC
        LIMIT %s
    """, (batch_size,))
    
    rows = cur.fetchall()

    if not rows:
        print("No customers found.")
        return

    # Apply segment-based probability
    eligible = []
    for row in rows:
        customer_id, country, city, segment, engagement_score = row
        prob = SEGMENT_UPDATE_PROB.get(segment, 0.5)

        if random.random() < prob:
            eligible.append(row)

    if not eligible:
        print("No customers selected after probability filter.")
        return

    # Pick subset to update
    to_update = random.sample(eligible, min(update_count, len(eligible)))

    for customer_id, country, city, segment, engagement_score in to_update:
        new_city = random.choice(COUNTRY_CITY_MAP.get(country, [city]))
        new_segment = random.choice(SEGMENTS)
        new_engagement = max(0, min(100, engagement_score + random.randint(-10, 10)))
        updated_at = datetime.now(timezone.utc)

        cur.execute("""
            UPDATE raw.customers
            SET city = %s,
                segment = %s,
                engagement_score = %s,
                updated_at = %s
            WHERE customer_id = %s
        """, (new_city, new_segment, new_engagement, updated_at, customer_id))

        print(f"[Customer] {customer_id}: "
              f"{city}/{segment}/{engagement_score} → "
              f"{new_city}/{new_segment}/{new_engagement}")

    conn.commit()
    cur.close()
    conn.close()

    print(f"Updated {len(to_update)} customers.")


# PRODUCT UPDATES
def update_products(batch_size=50, update_count=10):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT product_id, price, cost, stock_quantity, rating
        FROM raw.products
        ORDER BY updated_at DESC NULLS LAST, product_id DESC
        LIMIT %s
    """, (batch_size,))
    
    rows = cur.fetchall()

    if not rows:
        print("No products found.")
        return

    # Random subset (products don’t need segment logic)
    to_update = random.sample(rows, min(update_count, len(rows)))

    for product_id, price, cost, stock, rating in to_update:
        new_price = round(price * random.uniform(0.9, 1.1), 2)
        new_cost = round(cost * random.uniform(0.9, 1.1), 2)
        new_stock = max(0, stock + random.randint(-20, 20))
        new_rating = round(min(5, max(0, rating + random.uniform(-0.5, 0.5))), 1)
        updated_at = datetime.now(timezone.utc)

        cur.execute("""
            UPDATE raw.products
            SET price = %s,
                cost = %s,
                stock_quantity = %s,
                rating = %s,
                updated_at = %s
            WHERE product_id = %s
        """, (new_price, new_cost, new_stock, new_rating, updated_at, product_id))

        print(f"[Product] {product_id}: "
              f"price {price}->{new_price}, "
              f"cost {cost}->{new_cost}, "
              f"stock {stock}->{new_stock}, "
              f"rating {rating}->{new_rating}")

    conn.commit()
    cur.close()
    conn.close()

    print(f"Updated {len(to_update)} products.")


if __name__ == "__main__":
    update_customers(batch_size=100, update_count=20)
    update_products(batch_size=100, update_count=20)