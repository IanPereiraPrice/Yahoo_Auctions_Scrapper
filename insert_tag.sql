CREATE OR REPLACE FUNCTION public.insert_tag(_tag character varying)
 RETURNS void
 LANGUAGE plpgsql
AS $function$
        BEGIN
            INSERT INTO Yahoo_Auction_Tags(tag)
            VALUES(_tag);
        END;
    $function$
