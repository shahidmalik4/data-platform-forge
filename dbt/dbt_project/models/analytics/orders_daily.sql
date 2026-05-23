with orders as (

    select *
    from {{ ref('fact_orders') }}

)

select

    date_trunc('day', order_timestamp) as order_date,

    count(distinct order_id) as total_orders,
    count(distinct customer_id) as active_customers,

    sum(total_amount) as gross_revenue,
    sum(net_revenue) as net_revenue,
    sum(total_discount) as total_discount,
    sum(shipping_cost) as shipping_revenue,

    avg(total_amount) as avg_order_value,
    avg(total_items) as avg_items_per_order

from orders
group by 1