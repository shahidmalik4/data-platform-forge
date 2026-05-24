import dlt
from data_platform.ingestion.generators.generate_orders import run_order_generation
from data_platform.ingestion.utils.corrupt_data import corrupt_order


@dlt.resource(name="orders")
def orders_resource(orders):
    for order in orders:
        yield corrupt_order(order)