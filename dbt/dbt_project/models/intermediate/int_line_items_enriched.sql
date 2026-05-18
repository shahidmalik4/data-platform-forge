with items as (

    select *
    from {{ ref('fact_line_items') }}

),

products as (

    select *
    from {{ ref('dim_products') }}
    where dbt_valid_to is null

),

final as (

    select
        i.order_item_id,
        i.order_id,
        i.product_id,

        -- product info
        p.product_name,
        p.category,
        p.brand,

        -- metrics
        i.quantity,
        i.unit_price,
        i.gross_item_total,
        i.net_item_total

    from items i
    left join products p
        on i.product_id = p.product_id

)

select * from final