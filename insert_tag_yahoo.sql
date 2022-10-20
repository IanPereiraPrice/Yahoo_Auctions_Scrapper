CREATE OR REPLACE PROCEDURE public.insert_tag_yahoo(_tag character varying)
 LANGUAGE sql
AS $procedure$
    INSERT INTO Yahoo_Auction_Tags(Tag)
    VALUES(_tag);   
$procedure$
