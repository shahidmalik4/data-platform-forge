{{ config(
    materialized='table'
) }}

with source as (

    select *
    from {{ ref('stg_line_items') }}

),

final as (

    select

        -- GRAIN
        order_item_id,
        order_id,
        product_id,

        -- DIM ATTRIBUTES
        product_name,
        category,

        -- MEASURES
        quantity,
        unit_price,
        discount_pct,
        discount_amount,

        -- GROSS (must be repeated, no alias reuse)
        quantity * unit_price as gross_item_total,

        -- NET (computed directly from expression)
        round(quantity * unit_price - discount_amount, 2) as net_item_total,

        -- VALIDATION FLAG
        case
            when quantity > 0
             and unit_price > 0
             and product_id is not null
            then true
            else false
        end as is_valid_item,

        -- METADATA
        _dlt_id,
        _dlt_parent_id,
        _dlt_list_idx

    from source

)

select * from final