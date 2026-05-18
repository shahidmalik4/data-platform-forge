{% snapshot snap_dim_customers %}

{{
    config(
        target_schema='snapshots',
        unique_key='customer_id',

        strategy='timestamp',
        updated_at='updated_at'
    )
}}

SELECT
    customer_id,
    first_name,
    last_name,
    email,
    phone,
    city,
    country,
    segment,
    acquisition_channel,
    engagement_score,
    lifetime_value,
    is_active,
    last_login,
    signup_date,
    created_at,
    updated_at

FROM {{ ref('stg_customers') }}

{% endsnapshot %}