select

    category,
    product_name,

    sum(quantity) as total_units_sold,
    sum(net_item_total) as total_revenue,

    avg(unit_price) as avg_price

from {{ ref('int_line_items_enriched') }}

group by 1,2