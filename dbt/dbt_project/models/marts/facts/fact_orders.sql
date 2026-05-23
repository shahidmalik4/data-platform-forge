{{ config(
    materialized='incremental',
    unique_key='order_id',
    incremental_strategy='merge'
) }}

with source as (

    select *
    from {{ ref('stg_orders') }}

    {% if is_incremental() %}
        where updated_at > (select max(updated_at) from {{ this }})
    {% endif %}

),

final as (

select

    order_id,
    customer_id,
    customer_country,
    payment_method,

    total_items,
    total_amount,
    total_discount,
    shipping_cost,
    (total_amount - total_discount) as net_revenue,

    order_timestamp,
    shipping_timestamp,
    created_at,
    updated_at,
    delivery_days,
    order_status,

    case when order_status = 'completed' then 1 else 0 end as is_completed,
    case when order_status = 'pending' then 1 else 0 end as is_pending,
    case when order_status = 'shipped' then 1 else 0 end as is_shipped,

    case
        when order_status != 'cancelled'
        then 1 else 0
    end as is_valid_order,

    case
        when shipping_timestamp is not null
        then (
            shipping_timestamp::date
            - order_timestamp::date
        )
    end as fulfillment_time_days,

    _dlt_id,
    _dlt_load_id

from source

)

select * from final