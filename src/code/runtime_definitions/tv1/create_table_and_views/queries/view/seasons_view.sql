CREATE OR REPLACE VIEW tv_one.seasons_view
 AS
 SELECT season_id,
    program_id,
    season,
    url
   FROM tv_one.seasons;