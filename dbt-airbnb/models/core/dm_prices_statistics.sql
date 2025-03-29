with listings_data as (
    select * from {{ ref("fct_listings")}}
),

    price_percentiles as (
        select distinct country, city, room_type, 
            PERCENTILE_CONT(price, 0.30) over(partition by country, room_type) as p30_price_room_type_in_country,
            PERCENTILE_CONT(price, 0.75) over(partition by country, room_type) as p75_price_room_type_in_country,
            PERCENTILE_CONT(price, 0.95) over(partition by country, room_type) as p95_price_room_type_in_country,

            PERCENTILE_CONT(price, 0.30) over(partition by city, room_type) as p30_price_room_type_in_city,
            PERCENTILE_CONT(price, 0.75) over(partition by city, room_type) as p75_price_room_type_in_city,
            PERCENTILE_CONT(price, 0.95) over(partition by city, room_type) as p95_price_room_type_in_city
        from listings_data
),  

    price_levels as (
        select l.listing_id,   l.price,
                -- define price level 
                case 
                    when l.price <= p30_price_room_type_in_country 
                        then 'low cost'
                    when l.price > p30_price_room_type_in_country and l.price <= p75_price_room_type_in_country 
                        then 'middle cost'
                    when l.price > p95_price_room_type_in_country
                        then 'luxury'
                    else 'high cost' 
                end as price_level_country,
                case 
                    when l.price <= p30_price_room_type_in_city 
                        then 'low cost'
                    when l.price > p30_price_room_type_in_city and l.price <= p75_price_room_type_in_city 
                        then 'middle cost'
                    when l.price > p95_price_room_type_in_city
                        then 'luxury'
                    else 'high cost' 
                end as price_level_city               

        from listings_data l
        inner join price_percentiles p
            on l.country = p.country
            and l.city = p.city
            and l.room_type = p.room_type
)

    select ld.country, 
        ld.region, 
        ld.city,
        ld.release_year,
        ld.release_month, 
        ld.release_date,
        ld.listing_id,
        ld.latitude_longitude,
        ld.host_id,
        ld.room_type,
        ld.price,
        pl.price_level_country, 
        pl.price_level_city

from listings_data ld
inner join price_levels pl 
    on ld.listing_id = pl.listing_id

        
