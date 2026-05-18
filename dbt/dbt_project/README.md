# Data Platform (dbt Project)

This project models raw ecommerce data into analytics-ready datasets using dbt.

## Layers

### 1. Staging
- Cleaned raw data
- Type casting
- Standardization

### 2. Dimensions
- SCD Type 2 dimensions
- Surrogate keys
- Business entities

### 3. Facts
- Transactional metrics
- Business KPIs

## Models

- stg_customers
- stg_products
- stg_orders
- dim_customers
- dim_products
- fact_orders

## Data Quality

- Unique & not_null constraints
- Referential integrity tests
- Business logic validations

## How to run

```bash
dbt run
dbt test
dbt docs generate
dbt docs serve