select

    order_month,

    count(distinct order_id) as total_orders,
    count(distinct customer_id) as unique_customers,

    sum(total_amount) as gross_revenue,
    sum(net_revenue) as net_revenue,

    avg(total_amount) as avg_order_value,

    sum(case when order_status = 'completed' then 1 else 0 end) as completed_orders,
    sum(case when order_status = 'cancelled' then 1 else 0 end) as cancelled_orders

from {{ ref('int_orders_enriched') }}

group by 1