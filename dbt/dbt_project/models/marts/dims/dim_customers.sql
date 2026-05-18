with snapshot as (

    select * from {{ ref('snap_dim_customers') }}

),

final as (

    select
        -- Surrogate Key (SCD2 versioned)
        {{ dbt_utils.generate_surrogate_key([
            'customer_id',
            'dbt_valid_from'
        ]) }} as customer_sk,

        -- Natural key
        customer_id,

        -- attributes
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

        -- SCD2 metadata
        dbt_valid_from,
        dbt_valid_to,

        -- current flag
        case when dbt_valid_to is null then 1 else 0 end as is_current

    from snapshot

)

select * from final