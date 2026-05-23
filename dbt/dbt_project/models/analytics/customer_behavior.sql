with orders as (

    select *
    from {{ ref('fact_orders') }}

),

customer_stats as (

    select

        customer_id,

        count(order_id) as total_orders,
        sum(net_revenue) as lifetime_value,
        avg(total_amount) as avg_order_value,

        min(order_timestamp) as first_order,
        max(order_timestamp) as last_order

    from orders
    group by customer_id

)

select

    *,
    current_date - last_order::date as days_since_last_order,

    case
        when total_orders = 1 then 'one_time'
        when total_orders between 2 and 5 then 'regular'
        when total_orders > 5 then 'loyal'
    end as customer_segment,

    ntile(4) over (order by lifetime_value) as ltv_quartile

from customer_stats