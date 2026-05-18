{% snapshot snap_dim_products %}

{{
    config(
        target_schema='snapshots',
        unique_key='product_id',
        
        strategy='timestamp',
        updated_at='updated_at',
        invalidate_hard_deletes=True
    )
}}

select
    product_id,
    sku,
    product_name,
    category,
    subcategory,
    brand,
    price,
    cost,
    profit,
    stock_quantity,
    rating,
    is_active,
    created_at,
    updated_at

from {{ ref('stg_products') }}

{% endsnapshot %}