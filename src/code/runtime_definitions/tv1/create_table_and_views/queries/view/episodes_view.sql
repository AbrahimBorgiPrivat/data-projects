CREATE OR REPLACE VIEW tv_one.episodes_view
 AS
 SELECT episode_id,
    program_id,
    season_id,
        CASE
            WHEN TRIM(BOTH FROM split_part(details, '|'::text, 2)) ~~ '%m'::text THEN make_interval(mins => regexp_replace(TRIM(BOTH FROM split_part(details, '|'::text, 2)), '[^0-9]'::text, ''::text, 'g'::text)::integer)
            WHEN TRIM(BOTH FROM split_part(details, '|'::text, 2)) ~~ '%s'::text THEN make_interval(secs => regexp_replace(TRIM(BOTH FROM split_part(details, '|'::text, 2)), '[^0-9]'::text, ''::text, 'g'::text)::integer::double precision)
            ELSE NULL::interval
        END AS duration_interval,
    title,
    regexp_replace(title, '^(\d+)\..*'::text, '\1'::text)::integer AS episode_nr,
    details,
    url,
    description,
    image
   FROM tv_one.episodes e;