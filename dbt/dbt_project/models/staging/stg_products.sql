with source as (

    select * from {{ source('raw', 'products') }}

),

renamed as (

    select

        -- ids
        product_id::text as product_id,
        trim(sku) as sku,

        -- text cleanup
        trim(product_name) as product_name,
        coalesce(trim(category), 'unknown') as category,
        trim(subcategory) as subcategory,
        trim(brand) as brand,

        -- numeric
        case
            when nullif(trim(cast(price as text)), '')::numeric is null then 0
            when nullif(trim(cast(price as text)), '')::numeric < 0 then 0
            else nullif(trim(cast(price as text)), '')::numeric
        end as price,

        nullif(trim(cast(cost as text)), '')::numeric as cost,
        nullif(trim(cast(profit as text)), '')::numeric as profit,
        stock_quantity::integer as stock_quantity,
        rating::numeric as rating,

        -- boolean
        is_active::boolean as is_active,

        -- timestamps
        created_at::timestamp as created_at,
        updated_at::timestamp as updated_at,

        -- ingestion columns
        _dlt_load_id,
        _dlt_id

    from source

)

select *
from renamed