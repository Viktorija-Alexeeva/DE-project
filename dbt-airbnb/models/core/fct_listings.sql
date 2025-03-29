with france_listings as (
    select *  from {{ ref('stg_france_listings') }}
), 

    germany_listings as (
    select *  from {{ ref('stg_germany_listings') }}
), 

   greece_listings as (
    select *  from {{ ref('stg_greece_listings') }}
), 

   italy_listings as (
    select *  from {{ ref('stg_italy_listings') }}
), 

   portugal_listings as (
    select *  from {{ ref('stg_portugal_listings') }}
), 

   spain_listings as (
    select *  from {{ ref('stg_spain_listings') }}
), 

    listings_unioned as (
    select * from france_listings
        union all 
    select * from germany_listings
        union all 
    select * from greece_listings
        union all 
    select * from italy_listings
        union all 
    select * from portugal_listings
        union all 
    select * from spain_listings
)

select * 
from listings_unioned 
