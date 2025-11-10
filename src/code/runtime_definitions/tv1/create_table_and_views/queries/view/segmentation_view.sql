CREATE OR REPLACE VIEW tv_one.segmentation_view
 AS
 SELECT segmentation.segment_id,
    segmentation.segment_key,
    segmentation.name,
    segmentation.description,
    segmentation.activity_level
   FROM tv_one.segmentation;