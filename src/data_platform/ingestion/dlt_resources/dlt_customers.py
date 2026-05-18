import dlt
from data_platform.ingestion.generators.generate_customers import run_customer_generation
from data_platform.ingestion.utils.corrupt_data import corrupt_customer

@dlt.resource(name="customers")
def customers_resource():
    new_customers = run_customer_generation()
    for customer in new_customers:
        yield corrupt_customer(customer)