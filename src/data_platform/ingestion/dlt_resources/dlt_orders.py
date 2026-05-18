import dlt
from data_platform.ingestion.generators.generate_orders import run_order_generation
from data_platform.ingestion.utils.corrupt_data import corrupt_order, corrupt_order_item

@dlt.resource(name="orders")
def orders_resource():
    new_orders = run_order_generation()
    for order in new_orders:
        yield corrupt_order(order)