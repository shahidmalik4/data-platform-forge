import random
import uuid

# -------------------------------
# Helper functions
# -------------------------------
def maybe_null(record, field, prob=0.1):
    if field in record and random.random() < prob:
        record[field] = None
    return record

def maybe_outlier(record, field, prob=0.03):
    if field in record and isinstance(record[field], (int, float)) and random.random() < prob:
        record[field] *= random.choice([-10, 0, 100])
    return record

def maybe_mess_text(record, field, prob=0.05):
    if field in record and isinstance(record[field], str) and random.random() < prob:
        val = record[field]
        val = val.upper() if random.random() < 0.5 else val.lower()
        if random.random() < 0.3:
            val = " " + val
        if random.random() < 0.3:
            val = val + " "
        record[field] = val
    return record

def maybe_flip_relationship(record, field, prob=0.05, allow_fk_corruption=False):

    if not allow_fk_corruption:
        return record

    if field in record and random.random() < prob:
        record[field] = str(uuid.uuid4())

    return record

# -------------------------------
# Corrupt Customers
# -------------------------------
def corrupt_customer(customer):
    customer = maybe_null(customer, "email", 0.2)
    customer = maybe_null(customer, "phone", 0.15)
    customer = maybe_null(customer, "segment", 0.15)
    customer = maybe_null(customer, "last_name", 0.2)

    customer = maybe_mess_text(customer, "first_name", 0.2)
    customer = maybe_mess_text(customer, "last_name", 0.15)
    customer = maybe_mess_text(customer, "city", 0.15)
    customer = maybe_mess_text(customer, "country", 0.15)

    customer = maybe_outlier(customer, "lifetime_value", 0.2)
    customer = maybe_outlier(customer, "engagement_score", 0.2)

    return customer

# -------------------------------
# Corrupt Products
# -------------------------------
def corrupt_product(product):
    product = maybe_null(product, "brand", 0.1)
    product = maybe_null(product, "category", 0.15)

    product = maybe_mess_text(product, "product_name", 0.2)
    product = maybe_mess_text(product, "brand", 0.1)

    # Keep price numeric, but add outliers
    product = maybe_outlier(product, "price", 0.15)
    product = maybe_outlier(product, "cost", 0.2)

    return product

# -------------------------------
# Corrupt Order Items
# -------------------------------
def corrupt_order_item(item):
    item = maybe_null(item, "product_name", 0.1)
    item = maybe_null(item, "category", 0.1)

    item = maybe_mess_text(item, "product_name", 0.15)
    item = maybe_mess_text(item, "category", 0.1)

    item = maybe_outlier(item, "unit_price", 0.15)
    item = maybe_outlier(item, "item_total", 0.2)

    if "quantity" in item and random.random() < 0.1:
        item["quantity"] = max(1, item["quantity"] * random.choice([1, 2, 5]))

    item = maybe_outlier(item, "discount_amount", 0.15)

    # Cross-field corruption: item_total vs unit_price*quantity
    if "quantity" in item and "unit_price" in item and random.random() < 0.05:
        item["item_total"] = item["unit_price"] * item["quantity"] * random.choice([0.5, 1.5, 2])

    return item

# -------------------------------
# Corrupt Orders
# -------------------------------
def corrupt_order(order):
    order = maybe_null(order, "payment_method", 0.1)
    order = maybe_null(order, "shipping_timestamp", 0.15)

    order = maybe_outlier(order, "total_amount", 0.2)
    order = maybe_outlier(order, "total_discount", 0.1)
    order = maybe_outlier(order, "shipping_cost", 0.15)

    order = maybe_mess_text(order, "order_status", 0.1)
    order = maybe_mess_text(order, "payment_method", 0.15)
    order = maybe_mess_text(order, "customer_country", 0.2)

    # Corrupt nested items
    if "items" in order and isinstance(order["items"], list):
        order["items"] = [corrupt_order_item(i.copy()) for i in order["items"]]

    return order

# -------------------------------
# Corrupt list of records
# -------------------------------
def corrupt_list(records, record_type="customer"):
    corrupted = []
    for r in records:
        if record_type == "customer":
            corrupted.append(corrupt_customer(r.copy()))
        elif record_type == "product":
            corrupted.append(corrupt_product(r.copy()))
        elif record_type == "order":
            corrupted.append(corrupt_order(r.copy()))
        else:
            corrupted.append(r.copy())
    return corrupted