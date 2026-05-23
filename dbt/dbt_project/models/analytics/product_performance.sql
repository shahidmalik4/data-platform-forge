with items as (

    select *
    from {{ ref('fact_line_items') }}

)

select

    product_id,
    category,

    sum(quantity) as total_units_sold,
    sum(gross_item_total) as gross_revenue,
    sum(net_item_total) as net_revenue,

    avg(unit_price) as avg_selling_price,

    rank() over (order by sum(net_item_total) desc) as revenue_rank,
    dense_rank() over (partition by category order by sum(net_item_total) desc) as category_rank

from items
group by product_id, category