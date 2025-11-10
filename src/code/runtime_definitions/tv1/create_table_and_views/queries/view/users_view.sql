CREATE OR REPLACE VIEW tv_one.users_view
 AS
 SELECT users.user_id,
    users.age_group,
    users.household_size,
    users.region,
    users.children_under5,
    users.segment_id
   FROM tv_one.users;