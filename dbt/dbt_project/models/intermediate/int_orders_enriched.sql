with orders as (

    select *
    from {{ ref('fact_orders') }}

),

customers as (

    select *
    from {{ ref('dim_customers') }}
    where dbt_valid_to is null   -- current SCD2

),

final as (

    select
        o.order_id,
        o.customer_id,

        -- customer info
        c.first_name,
        c.last_name,
        c.country,
        c.segment,

        -- order info
        o.order_status,
        o.payment_method,
        o.total_amount,
        o.net_revenue,
        o.total_items,

        o.order_timestamp,
        o.delivery_days,

        -- derived
        date_trunc('month', o.order_timestamp) as order_month

    from orders o
    left join customers c
        on o.customer_id = c.customer_id

)

select * from final