CREATE OR REPLACE VIEW gamma_db.postering_group_view
 AS
 SELECT postering_group.id,
    postering_group.posting_group,
    postering_group.posting_group_key,
    postering_group.posting_sub_group,
    postering_group.posting_sub_group_key,
    postering_group.context,
    postering_group.context_key
   FROM gamma_db.postering_group;