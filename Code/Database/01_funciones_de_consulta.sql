CREATE FUNCTION get_user_by_id(id INT) RETURNS "User" AS
  $$
    SELECT id, username, email, name, bio, password FROM "User" WHERE id = $1;
  $$ LANGUAGE sql;

CREATE FUNCTION get_user_by_username(username VARCHAR(75)) RETURNS "User" AS
  $$
    SELECT id, username, email, name, bio, password FROM "User" WHERE username = $1;
  $$ LANGUAGE sql;


CREATE FUNCTION get_user_by_mail(mail VARCHAR(75)) RETURNS "User" AS
  $$
    SELECT id, username, email, name, bio, password FROM "User" WHERE email = $1;
  $$ LANGUAGE sql;
  
CREATE type user_public_info as (id int, username VARCHAR(75), name VARCHAR(200), bio TEXT);

CREATE FUNCTION get_followed_by_user(id INT, lim INT, ofset INT) RETURNS SETOF user_public_info AS
  $$
    SELECT u.id, u.username, u.name, u.bio
    FROM "User" u, follower f
    WHERE u.id = f.followedid AND f.userid = $1
    LIMIT $2
    OFFSET $3;
  $$ LANGUAGE sql;
  
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

CREATE FUNCTION get_album_by_id(id INT, lim INT, ofset INT) RETURNS album AS
  $$
    SELECT *
    FROM album
    WHERE id = $1
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

CREATE FUNCTION get_album_by_authorid(id INT, lim INT, ofset INT) RETURNS SETOF album AS
  $$
    SELECT *
    FROM album
    WHERE authorid = $1
    LIMIT lim
    OFFSET ofset;
  $$ LANGUAGE sql;

CREATE FUNCTION get_author_name_by_id(id INT) RETURNS VARCHAR(75) AS
  $$
    SELECT name
    FROM author
    WHERE id = $1;
  $$ LANGUAGE sql;
  
CREATE FUNCTION get_users_by_name(query VARCHAR(75), lim INT, ofset INT) RETURNS SETOF user_public_info AS
  $$
    SELECT id, username, name, bio
    FROM "User"
    WHERE name ILIKE '%' || query || '%'
    LIMIT lim
    OFFSET ofset;
  $$ LANGUAGE sql;

CREATE FUNCTION get_users_by_username(query VARCHAR(75), lim INT, ofset INT) RETURNS SETOF user_public_info AS
  $$
    SELECT id, username, name, bio
    FROM "User"
    WHERE username ILIKE '%' || query || '%'
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
  
CREATE FUNCTION insert_new_play_list(name VARCHAR(75), userid INT, bio text) RETURNS BOOLEAN AS
  $$
  BEGIN
    IF userid IN (SELECT id FROM "User") THEN
      INSERT INTO list (name, userid, creationdate, description)
      VALUES ($1,$2,current_date,$3);
      RETURN FOUND;
    ELSE
      RETURN FALSE;
    END IF;
  END;
  $$ LANGUAGE plpgsql;
  
CREATE FUNCTION insert_new_user(username VARCHAR(75), mail VARCHAR(75), name VARCHAR(200), password VARCHAR(200)) RETURNS BOOLEAN AS
  $$
  DECLARE
    new_id INT;
  BEGIN
    IF mail NOT IN (SELECT u.email FROM "User" u) THEN
      INSERT INTO "User" (username, email, name, password)
      VALUES ($1, $2, $3, $4)
      RETURNING id INTO new_id;
      RETURN insert_new_play_list('Favoritos', new_id, 'Tu música favorita');
    ELSE
      RETURN FALSE;
    END IF;
  END;
  $$ LANGUAGE plpgsql;
  
CREATE FUNCTION follow_user(actual INT, followed INT) RETURNS BOOLEAN AS
  $$
  BEGIN
    IF (actual IN (SELECT id FROM "User")) AND (followed IN (SELECT id FROM "User")) THEN
      IF actual NOT IN (SELECT userid FROM follower WHERE userid = actual AND followedid = followed) THEN
        INSERT INTO follower VALUES (actual, followed);
        RETURN FOUND;
      ELSE
        RETURN FALSE;
      END IF;
    ELSE
      RETURN FALSE;
    END IF;
  END;
  $$ LANGUAGE plpgsql;
  
CREATE FUNCTION insert_song_in_list(list INT, song INT) RETURNS BOOLEAN AS
  $$
  BEGIN
    IF (list IN (SELECT id FROM list)) AND (song IN (SELECT id FROM song)) THEN
      IF list NOT IN (SELECT listid FROM listsong WHERE listid = $1 AND songid = song) THEN
        INSERT INTO listsong VALUES ($1, song);
        RETURN FOUND;
      ELSE
        RETURN FALSE;
      END IF;
    ELSE
      RETURN FALSE;
    END IF;
  END;
  $$ LANGUAGE plpgsql;
