with 

source as (

    select * ,
        case 
            when region = 'lombardia' 
                then 'lombardy'
            else region
        end as region_updated,
        case 
            when license is null then 0 
                else 1
        end as has_license ,
        concat(latitude, ',' , longitude) as latitude_longitude
    from {{ source('staging', 'italy_listings') }}
    where price is not null

),

renamed as (

    select
        INITCAP(country) as country,
        INITCAP(region_updated) as region,
        INITCAP(city) as city,        
        EXTRACT(YEAR FROM release_date) AS release_year,
        EXTRACT(MONTH FROM release_date) AS release_month,
        release_date,
        COALESCE(id, CAST( {{ dbt_utils.generate_surrogate_key(['city', 'neighbourhood','latitude', 'longitude']) }} as INT64)) as listing_id,
        name as listing_name,
        host_id,
        host_name,
        neighbourhood_group,
        neighbourhood,
        latitude_longitude,
        room_type,
        price,
        minimum_nights,
        number_of_reviews,
        last_review,
        reviews_per_month,
        calculated_host_listings_count,
        availability_365,
        number_of_reviews_ltm,
        cast(has_license as BOOLEAN) as has_license        

    from source

)

select * from renamed
