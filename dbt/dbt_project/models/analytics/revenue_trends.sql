with daily as (

    select
        date_trunc('day', order_timestamp) as order_date,
        sum(net_revenue) as net_revenue
    from {{ ref('fact_orders') }}
    group by 1

)

select

    order_date,
    net_revenue,

    avg(net_revenue) over (
        order by order_date
        rows between 6 preceding and current row
    ) as moving_7d_avg,

    sum(net_revenue) over (
        order by order_date
        rows between unbounded preceding and current row
    ) as cumulative_revenue

from daily