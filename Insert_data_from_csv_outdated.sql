WITH cte AS(
    SELECT 
        product_name AS title
        , (LEFT("dmg_sold"."auction_end_time",10)||' '||RIGHT("dmg_sold"."auction_end_time",5)) AS auction_end
        , (LEFT("dmg_sold"."auction_start_time",10)||' '||RIGHT("dmg_sold"."auction_start_time",5)) AS auction_start
        , regexp_replace(final_price, '\D+', '', 'g')::int AS price1
        ,number_of_bids::int as bids
        ,sigh
    FROM dmg_sold)
,cte2 AS (
    SELECT 
        *
        , regexp_replace(price, '\D+', '', 'g')::int AS price1
    FROM "Card_Sales_Staging"
)

,cte3 AS (
    SELECT 
        id
        ,title
        ,sigh
    FROM cte2
    INNER JOIN cte
    USING(title,price1,auction_end,auction_start)
    )

,cte4 AS (SELECT * 
FROM "Card_Sales_Staging"
WHERE auction_id in (
    SELECT auction_id
    FROM cte3)
)

INSERT INTO "Card_Sales_Staging"(auction_id, title,price, bids, tax,auction_start,auction_end,auction_extension,best_offer_accepted,all_images)
(SELECT 
    'ZZZ'||FLOOR(RANDOM()*(99999999-10000000+1)+10000000) AS auction_id
    ,product_name AS title
    ,final_price AS price
    ,number_of_bids::INT AS bids
    ,tax
    ,auction_start_time AS auction_start
    ,auction_end_time AS auction_end
    ,auction_extension
    ,best_offer_accepted
    ,images AS all_images
FROM dmg_sold
WHERE sigh NOT in (
    SELECT sigh
    FROM cte3)
)
