with source as (

    select *
    from {{ source('raw', 'orders__items') }}

),

cleaned as (

    select

        -- KEYS
        nullif(trim(order_item_id), '') as order_item_id,
        nullif(trim(order_id), '') as order_id,
        nullif(trim(product_id), '') as product_id,

        -- ATTRIBUTES
        lower(trim(product_name)) as product_name,
        lower(trim(category)) as category,

        -- MEASURES
        nullif(trim(cast(quantity as text)), '')::numeric as quantity,
        nullif(trim(cast(unit_price as text)), '')::numeric as unit_price,
        nullif(trim(cast(item_total as text)), '')::numeric as item_total,

        coalesce(nullif(trim(cast(discount_pct as text)), '')::numeric, 0) as discount_pct,
        coalesce(nullif(trim(cast(discount_amount as text)), '')::numeric, 0) as discount_amount,

        -- METADATA
        _dlt_parent_id,
        _dlt_list_idx,
        _dlt_id

    from source

),

validated as (

    select *

    from cleaned

    where order_item_id is not null
      and order_id is not null
      and product_id is not null
      and quantity is not null
      and quantity > 0
      and unit_price is not null
      and unit_price > 0

)

select *
from validated