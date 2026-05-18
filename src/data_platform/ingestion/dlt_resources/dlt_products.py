import dlt
from data_platform.ingestion.generators.generate_products import run_product_generation
from data_platform.ingestion.utils.corrupt_data import corrupt_product

@dlt.resource(name="products")
def products_resource():
    new_products = run_product_generation()
    for product in new_products:
        yield corrupt_product(product)