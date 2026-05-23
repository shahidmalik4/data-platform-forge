select
    customer_id,

    count(distinct order_id) as total_orders,
    sum(net_revenue) as lifetime_value,
    avg(total_amount) as avg_order_value

from {{ ref('fact_orders') }}
group by 1