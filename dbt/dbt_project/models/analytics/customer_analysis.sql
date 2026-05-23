with customers as (

    select
        customer_id,
        sum(net_revenue) as revenue
    from {{ ref('fact_orders') }}
    group by 1

),

ranked as (

    select
        *,
        sum(revenue) over (order by revenue desc) as running_revenue,
        sum(revenue) over () as total_revenue
    from customers

)

select
    *,
    running_revenue / total_revenue as revenue_share
from ranked