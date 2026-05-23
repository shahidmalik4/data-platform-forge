with orders as (

    select *
    from {{ ref('fact_orders') }}

),

base as (

    select
        *,
        avg(net_revenue) over () as global_avg_order_value,
        net_revenue - avg(net_revenue) over () as vs_average_order_value
    from orders

)

select * from base