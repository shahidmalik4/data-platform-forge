with source as (

    select *
    from {{ source('raw', 'orders') }}

),

renamed as (

    select

        -- KEYS
        order_id::text as order_id,
        customer_id::text as customer_id,

        -- attributes
        trim(customer_country) as customer_country,
        lower(trim(order_status)) as order_status,
        trim(payment_method) as payment_method,

        -- timestamps
        order_timestamp::timestamp as order_timestamp,
        shipping_timestamp::timestamp as shipping_timestamp,
        created_at::timestamp as created_at,
        updated_at::timestamp as updated_at,

        -- measures
        delivery_days::integer as delivery_days,
        total_items::integer as total_items,

        -- numeric
        coalesce(total_amount::numeric, 0) as total_amount,
        coalesce(total_discount::numeric, 0) as total_discount,
        coalesce(shipping_cost::numeric, 0) as shipping_cost,

        -- metadata
        _dlt_load_id,
        _dlt_id

    from source

)

select *
from renamed