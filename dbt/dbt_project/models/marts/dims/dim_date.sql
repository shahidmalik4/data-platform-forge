with date_spine as (

    select
        (
            current_date - interval '5 years'
            + (n || ' days')::interval
        )::date as date_day

    from generate_series(0, 3649) as t(n)

)

select

    -- Key
    to_char(date_day, 'YYYYMMDD')::integer as date_key,

    -- Parts
    extract(day from date_day) as day_of_month,

    extract(dow from date_day) as day_of_week_num,

    trim(to_char(date_day, 'Day')) as day_name,

    extract(doy from date_day) as day_of_year,

    extract(week from date_day) as iso_week,

    extract(week from date_day) as week_of_year,

    extract(month from date_day) as month,

    trim(to_char(date_day, 'Month')) as month_name,

    extract(quarter from date_day) as quarter,

    'Q' || extract(quarter from date_day) as quarter_name,

    extract(year from date_day) as year,

    -- Formats
    to_char(date_day, 'YYYY-MM') as year_month,

    (
        extract(year from date_day)::integer * 100
        + extract(month from date_day)::integer
    ) as year_month_int,

    to_char(date_day, 'IYYY-IW') as year_week,

    -- Boundaries
    date_trunc('week', date_day)::date as week_start_date,

    (
        date_trunc('week', date_day)
        + interval '6 days'
    )::date as week_end_date,

    date_trunc('month', date_day)::date as month_start_date,

    (
        date_trunc('month', date_day)
        + interval '1 month'
        - interval '1 day'
    )::date as month_end_date,

    -- Flags
    extract(dow from date_day) in (0, 6) as is_weekend,

    extract(dow from date_day) not in (0, 6) as is_weekday,

    date_day = date_trunc('month', date_day)::date as is_month_start,

    date_day = (
        date_trunc('month', date_day)
        + interval '1 month'
        - interval '1 day'
    )::date as is_month_end

from date_spine