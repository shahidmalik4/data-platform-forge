from generate_customers import run_customer_generation
from generate_products import run_product_generation
from generate_orders import run_order_generation

def main():
    # Customers
    new_cust = run_customer_generation()
    print(f"Customers -> Added: {len(new_cust)}")

    # Products
    new_prod = run_product_generation()
    print(f"Products -> Added: {len(new_prod)}")

    # Orders
    new_orders = run_order_generation()
    print(f"Orders -> Added: {len(new_orders)}")

if __name__ == "__main__":
    main()