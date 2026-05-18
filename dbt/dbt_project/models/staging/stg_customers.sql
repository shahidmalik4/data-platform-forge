with source as (

    select * from {{ source('raw', 'customers') }}

),

renamed as (

    select

        -- ids
        customer_id::text as customer_id,

        -- text cleanup
        trim(first_name) as first_name,
        trim(last_name) as last_name,
        coalesce(lower(trim(email)), 'unknown') as email,
        trim(phone) as phone,
        trim(city) as city,
        coalesce(trim(country), 'unknown') as country,
        trim(segment) as segment,
        trim(acquisition_channel) as acquisition_channel,

        -- dates
        signup_date::date as signup_date,
        last_login::timestamp as last_login,
        created_at::timestamp as created_at,
        updated_at::timestamp as updated_at,

        -- numeric
        lifetime_value::numeric as lifetime_value,
        engagement_score::numeric as engagement_score,

        -- boolean
        is_active::boolean as is_active,

        -- dlt metadata
        _dlt_load_id,
        _dlt_id

    from source

)

select *
from renamed
where customer_id is not null