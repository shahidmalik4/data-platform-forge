import uuid
import random
from datetime import datetime
from faker import Faker
import os

from data_platform.ingestion.utils.db_utils import fetch_table, is_first_run
from data_platform.ingestion.utils.corrupt_data import corrupt_list

fake = Faker()

NO_OF_CUSTOMERS = 250
NO_NEW_CUSTOMERS = 7


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


def generate_email(first_name, last_name):
    domains = ["gmail.com", "yahoo.com", "outlook.com"]
    return f"{first_name.lower()}.{last_name.lower()}{random.randint(1,999)}@{random.choice(domains)}"


def create_customer():
    country = random.choice(list(COUNTRY_CITY_MAP.keys()))
    city = random.choice(COUNTRY_CITY_MAP[country])

    first_name = fake.first_name()
    last_name = fake.last_name()

    signup_date = fake.date_between(start_date="-2y")

    is_active = random.choices([True, False], weights=[0.85, 0.15])[0]

    last_login = (
        fake.date_time_between(start_date=signup_date)
        if is_active
        else fake.date_time_between(start_date="-180d", end_date="-30d")
    )

    return {
        "customer_id": str(uuid.uuid4()),
        "first_name": first_name,
        "last_name": last_name,
        "email": generate_email(first_name, last_name),
        "phone": fake.phone_number(),
        "city": city,
        "country": country,
        "signup_date": signup_date.isoformat(),
        "last_login": last_login.isoformat(),
        "segment": random.choice(["free", "pro", "enterprise"]),
        "lifetime_value": round(random.uniform(0, 5000), 2),
        "engagement_score": random.randint(1, 100),
        "acquisition_channel": random.choice(["organic", "ads", "referral", "social", "email"]),
        "is_active": is_active,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }


# -------------------------------
# MAIN LOGIC FIX
# -------------------------------
# def run_customer_generation():
#     existing = fetch_table("customers")
#     first_run = is_first_run("customers")

#     if first_run:
#         return [create_customer() for _ in range(NO_OF_CUSTOMERS)]
#     else:
#         return [create_customer() for _ in range(NO_NEW_CUSTOMERS)]


def run_customer_generation():
    customers = [create_customer() for _ in range(NO_OF_CUSTOMERS)]

    # Add corruption
    if os.getenv("DATA_MODE") == "chaos":
        customers = corrupt_list(customers, record_type="customer")

    return customers