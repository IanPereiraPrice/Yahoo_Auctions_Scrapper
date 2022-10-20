CREATE OR REPLACE PROCEDURE public.insert_items_tags_2(_tag text)
 LANGUAGE sql
AS $procedure$ 


-- Check if inputs are in translation table. If not, attempts to match the inputs to the tag table directly
WITH cte_main AS(
    SELECT id, '%'||japanese||'%' AS japanese
    FROM japanese_translations
    LEFT JOIN "yahoo_auction_tags"
    ON "yahoo_auction_tags".tag = japanese_translations.english
    WHERE english=_tag
   
    
)
INSERT INTO
    "items_tags" (Auction_id, tag_id)
-- Matches inputs to the titles and then returns auction_id and tag_id. *** Inputs need to be surrounded by % % in order to match tags anywhere in the title. Must also put _ in if required for search, ie PSA_10 to be more robust in matching
SELECT
    auction_id,
    tag_id
FROM(
        SELECT
            auction_id,
            CASE
                WHEN title LIKE ANY(
                    SELECT japanese
                    FROM cte_main) 
                THEN (
                    SELECT
                        id
                    FROM
                        cte_main
                    GROUP BY id
                    )
                ELSE 0
            END AS tag_id
        FROM
            "Card_Sales_Staging"
    ) AS sub
WHERE
    tag_id != 0;
$procedure$
