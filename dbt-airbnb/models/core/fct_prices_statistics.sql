with listings_data as (
    select * from {{ ref("dim_listings")}}
)

select country, 
        region, 
        city,
        release_year,
        release_month, 
        release_date,
        listing_id,
        host_id,
        room_type,
        price,

        -- avg, min and max prices
        round( avg(price) over(partition by country, room_type), 2) as avg_price_room_type_in_country,
        min(price) over(partition by country, room_type) as min_price_room_type_in_country,
        max(price) over(partition by country, room_type) as max_price_room_type_in_country,

        round( avg(price) over(partition by city, room_type), 2) as avg_price_room_type_in_city,
        min(price) over(partition by city, room_type) as min_price_room_type_in_city,
        max(price) over(partition by city, room_type) as max_price_room_type_in_city,

        -- Standard Deviation of Price (It helps to understand the price variability in a given group (country, city, room type, etc.).)
        round( stddev(price) over(partition by country, room_type), 2) as stddev_price_room_type_in_country,
        round( stddev(price) over(partition by city, room_type), 2) as stddev_price_room_type_in_city,

        -- Price Percentiles (Useful for seeing how prices are distributed. )
        PERCENTILE_CONT(price, 0.25) over(partition by country, room_type) as p25_price_room_type_in_country,
        PERCENTILE_CONT(price, 0.5) over(partition by country, room_type) as p50_price_room_type_in_country,
        PERCENTILE_CONT(price, 0.75) over(partition by country, room_type) as p75_price_room_type_in_country,

        PERCENTILE_CONT(price, 0.25) over(partition by city, room_type) as p25_price_room_type_in_city,
        PERCENTILE_CONT(price, 0.5) over(partition by city, room_type) as p50_price_room_type_in_city,
        PERCENTILE_CONT(price, 0.75) over(partition by city, room_type) as p75_price_room_type_in_city,

        -- number of listings
        count(listing_id) over(partition by country, room_type) as number_of_listings_for_room_type_in_country,
        count(listing_id) over(partition by city, room_type) as number_of_listings_for_room_type_in_city

from listings_data 

