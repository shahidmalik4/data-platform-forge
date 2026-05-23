with orders as (

    select *
    from {{ ref('fact_orders') }}

)

select

    count(distinct order_id) as total_orders,
    sum(total_amount) as total_revenue,
    sum(net_revenue) as net_revenue,
    sum(total_discount) as total_discount,

    sum(total_amount) / nullif(count(distinct order_id), 0) as avg_order_value,
    sum(total_discount) / nullif(sum(total_amount), 0) as discount_rate,

    avg(fulfillment_time_days) as avg_fulfillment_time,
    avg(total_items) as avg_items_per_order

from orders