with snapshot as (

    select * from {{ ref('snap_dim_products') }}

),

final as (

    select

        -- Surrogate key (SCD2 version)
        {{ dbt_utils.generate_surrogate_key([
            'product_id',
            'dbt_valid_from'
        ]) }} as product_sk,

        -- natural key
        product_id,
        sku,
        product_name,
        category,
        subcategory,
        brand,

        price,
        cost,
        profit,
        stock_quantity,
        rating,

        created_at,
        updated_at,

        -- SCD2 fields
        dbt_valid_from,
        dbt_valid_to,

        -- current flag (BEST PRACTICE)
        case when dbt_valid_to is null then 1 else 0 end as is_current

    from snapshot

)

select * from final