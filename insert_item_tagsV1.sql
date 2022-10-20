CREATE OR REPLACE PROCEDURE public.insert_items_tags(VARIADIC tag_list character varying[])
 LANGUAGE sql
AS $procedure$ 

-- Use first element of input array to translate tags from translations table to match on tags
WITH cte_sub AS (
    SELECT
        tag
    FROM
        "yahoo_auction_tags"
    WHERE
        tag = (
            SELECT
                ENGLISH
            FROM
                "japanese_translations"
            WHERE
                japanese = REPLACE(tag_list [1], '%', '')
        )
),
-- Check if inputs are in translation table. If not, attempts to match the inputs to the tag table directly
cte_main AS(
    SELECT
        CASE
            WHEN (
                SELECT
                    COUNT(tag)
                FROM
                    cte_sub
            ) = 1 THEN (
                SELECT
                    tag
                FROM
                    cte_sub
            )
            ELSE (
                SELECT
                    "yahoo_auction_tags".tag
                FROM
                    "yahoo_auction_tags"
                WHERE
                    "yahoo_auction_tags".tag = REPLACE(tag_list [1], '%', '')
            )
        END AS tag
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
                WHEN title ILIKE ANY(tag_list) THEN (
                    SELECT
                        id
                    FROM
                        "yahoo_auction_tags"
                    WHERE
                        tag = (
                            SELECT
                                *
                            FROM
                                cte_main
                        )
                )
                ELSE 0
            END AS tag_id
        FROM
            "Card_Sales_Staging"
    ) AS sub
WHERE
    tag_id != 0;
$procedure$
