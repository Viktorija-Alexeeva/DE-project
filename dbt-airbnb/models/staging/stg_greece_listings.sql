with 

source as (

    select * ,
        case 
            when license is null then 0 
                else 1
        end as has_license  
    from {{ source('staging', 'greece_listings') }}
    where price is not null

),

renamed as (

    select
        INITCAP(country) as country,
        INITCAP(region) as region,
        INITCAP(city) as city,        
        EXTRACT(YEAR FROM release_date) AS release_year,
        EXTRACT(MONTH FROM release_date) AS release_month,
        release_date,
        id as listing_id,
        name as listing_name,
        host_id,
        host_name,
        neighbourhood_group,
        neighbourhood,
        latitude,
        longitude,
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
