import uuid
import random
from datetime import datetime, timedelta
from faker import Faker

from data_platform.ingestion.utils.db_utils import fetch_table, is_first_run
from data_platform.ingestion.utils.order_item_buckets import realistic_num_items

fake = Faker()

# -------------------------------
# CONFIG
# -------------------------------
NO_OF_ORDERS_FIRST_RUN = 2000
NO_NEW_ORDERS = 35

PAYMENT_METHODS = {
    "United States": ["credit_card", "paypal"],
    "United Kingdom": ["credit_card", "paypal"],
    "Germany": ["credit_card", "bank_transfer"],
    "Pakistan": ["cash_on_delivery", "bank_transfer"],
    "Saudi Arabia": ["credit_card", "mada"],
    "UAE": ["credit_card", "cash_on_delivery"]
}

# -------------------------------
# HELPERS
# -------------------------------
def pick_customer(customers):
    weights = [
        max(1, c.get("engagement_score", 50))
        for c in customers
    ]
    return random.choices(customers, weights=weights, k=1)[0]


def pick_product(products):
    weights = [
        1 / max(p.get("price", 1), 1)
        for p in products
    ]
    return random.choices(products, weights=weights, k=1)[0]


def validate_customers(customers):
    valid = [
        c for c in customers
        if c.get("customer_id")
        and isinstance(c.get("engagement_score"), (int, float))
    ]

    print(f"[INFO] Customers fetched: {len(customers)} | Valid: {len(valid)}")

    if not valid:
        raise ValueError("Customer data contract violated")

    return valid


def validate_products(products):
    valid = [
        p for p in products
        if p.get("product_id")
        and isinstance(p.get("price"), (int, float))
    ]

    print(f"[INFO] Products fetched: {len(products)} | Valid: {len(valid)}")

    if not valid:
        raise ValueError("Product data contract violated")

    return valid


def get_quantity(category):
    if category == "Electronics":
        return 1
    elif category == "Clothing":
        return random.randint(1, 3)
    return random.randint(1, 5)


def get_order_status(order_timestamp):
    days = (datetime.utcnow() - order_timestamp).days
    if days < 2:
        return "pending"
    elif days < 7:
        return "shipped"
    return "delivered"


# -------------------------------
# ORDER CREATION
# -------------------------------
def create_order(customers, products):
    customer = pick_customer(customers)
    order_id = str(uuid.uuid4())

    order_timestamp = fake.date_time_between(start_date="-1y", end_date="now")
    status = get_order_status(order_timestamp)

    country = (customer.get("country") or "").strip()
    payment_method = random.choice(
        PAYMENT_METHODS.get(country, ["credit_card"])
    )

    num_items = realistic_num_items()

    order_items = []

    total_gross = 0
    total_discount = 0

    for _ in range(num_items):
        product = pick_product(products)

        quantity = get_quantity(product.get("category", "Other"))
        unit_price = float(product.get("price") or 0)

        gross_item_total = round(unit_price * quantity, 2)

        discount_pct = random.choice([0, 5, 10, 15])
        discount_amount = round(gross_item_total * discount_pct / 100, 2)

        net_item_total = round(gross_item_total - discount_amount, 2)

        total_gross += gross_item_total
        total_discount += discount_amount

        order_items.append({
            "order_item_id": str(uuid.uuid4()),
            "order_id": order_id,

            "product_id": product["product_id"],
            "product_name": product["product_name"],
            "category": product["category"],

            "quantity": quantity,
            "unit_price": unit_price,

            # CLEAN ACCOUNTING MODEL
            "gross_item_total": gross_item_total,
            "discount_pct": discount_pct,
            "discount_amount": discount_amount,
            "net_item_total": net_item_total
        })

    shipping_cost = round(random.uniform(0, 20), 2)

    shipping_timestamp = (
        order_timestamp + timedelta(days=random.randint(1, 5))
        if status in ["shipped", "delivered"]
        else None
    )

    delivery_days = (
        random.randint(1, 5) if shipping_timestamp else None
    )

    return {
        "order_id": order_id,
        "customer_id": customer["customer_id"],

        "customer_country": customer["country"],
        "order_status": status,
        "payment_method": payment_method,

        "order_timestamp": order_timestamp.isoformat(),
        "shipping_timestamp": shipping_timestamp.isoformat() if shipping_timestamp else None,
        "delivery_days": delivery_days,

        "items": order_items,

        "total_items": num_items,

        # GROSS + DISCOUNT ONLY (dbt derives net_revenue)
        "total_amount": round(total_gross, 2),
        "total_discount": round(total_discount, 2),
        "shipping_cost": shipping_cost,

        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }


# -------------------------------
# MAIN RUN
# -------------------------------
def run_order_generation():
    raw_customers = fetch_table("customers")
    raw_products = fetch_table("products")

    if not raw_customers or not raw_products:
        raise ValueError("Missing customers/products data in RAW layer")

    customers = validate_customers(raw_customers)
    products = validate_products(raw_products)

    first_run = is_first_run("orders")
    n_orders = NO_OF_ORDERS_FIRST_RUN if first_run else NO_NEW_ORDERS

    return [
        create_order(customers, products)
        for _ in range(n_orders)
    ]