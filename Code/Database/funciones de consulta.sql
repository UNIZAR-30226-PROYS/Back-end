CREATE FUNCTION get_user_by_id(id INT) RETURNS "User" AS
  $$
    SELECT id, username, email, name, bio, password FROM "User" WHERE id = $1;
  $$ LANGUAGE sql;
  
CREATE type user_public_info as (id int, username VARCHAR(75), name VARCHAR(200), bio TEXT);

CREATE FUNCTION get_followed_by_user(id INT, lim INT, ofset INT) RETURNS SETOF user_public_info AS
  $$
    SELECT u.id, u.username, u.name, u.bio
    FROM "User" u, follower f
    WHERE u.id = f.followedid AND f.userid = $1
    LIMIT $2
    OFFSET $3;
  $$ LANGUAGE sq
  
CREATE FUNCTION get_followers_by_user(id INT, lim INT, ofset INT) RETURNS SETOF user_public_info AS
  $$
    SELECT u.id, u.username, u.name, u.bio
    FROM "User" u, follower f
    WHERE u.id = f.userid AND f.followedid = $1
    LIMIT $2
    OFFSET $3;
  $$ LANGUAGE sql;
  
CREATE FUNCTION get_list_by_ownerid(id INT, lim INT, ofset INT) RETURNS SETOF list AS
  $$
    SELECT *
    FROM list
    WHERE userid = $1
    LIMIT $2
    OFFSET $3;
  $$ LANGUAGE sql;
  
CREATE FUNCTION get_list_by_id(id INT) RETURNS list AS
  $$
    SELECT *
    FROM list
    WHERE id = $1;
  $$ LANGUAGE sql;
  
CREATE FUNCTION get_album_by_publish_year(year INT, lim INT, ofset INT) RETURNS album AS
  $$
    SELECT *
    FROM album
    WHERE EXTRACT(YEAR FROM publishdate) = $1
    LIMIT $2
    OFFSET $3;
  $$ LANGUAGE sql;

CREATE FUNCTION get_album_by_name(a_name VARCHAR(75), lim INT, ofset INT) RETURNS SETOF album AS
  $$
    SELECT *
    FROM album
    WHERE name ILIKE '%' || a_name || '%'
    LIMIT lim
    OFFSET ofset;
  $$ LANGUAGE sql;
 
CREATE FUNCTION get_author_name_by_id(id INT) RETURNS VARCHAR(75) AS
  $$
    SELECT name
    FROM author
    WHERE id = $1;
  $$ LANGUAGE sql;
  
CREATE FUNCTION get_users_by_parameter(query VARCHAR(75), lim INT, ofset INT) RETURNS SETOF user_public_info AS
  $$
    SELECT id, username, name, bio
    FROM "User"
    WHERE name ILIKE '%' || query || '%'
          OR
          username ILIKE '%' || query || '%'
    LIMIT lim
    OFFSET ofset;
  $$ LANGUAGE sql;
  
CREATE FUNCTION get_authors_by_name(query VARCHAR(75), lim INT, ofset INT) RETURNS SETOF author AS
  $$
    SELECT *
    FROM author
    WHERE name ILIKE '%' || query || '%'
    LIMIT lim
    OFFSET ofset;
  $$ LANGUAGE sql;
