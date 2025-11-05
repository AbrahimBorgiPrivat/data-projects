CREATE OR REPLACE VIEW tv_one.programs_view
 AS
 SELECT program_id,
    title,
    category,
    seasons,
    url,
    image
   FROM tv_one.programs;