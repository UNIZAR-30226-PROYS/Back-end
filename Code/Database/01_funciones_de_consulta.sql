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

CREATE FUNCTION get_album_by_id(id INT) RETURNS album AS
  $$
    SELECT *
    FROM album
    WHERE id = $1;
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
  
CREATE FUNCTION insert_new_artist(in_name VARCHAR(75), in_bio TEXT, path_image Text) RETURNS BOOLEAN AS
  $$
  DECLARE
    new_id INT;
  BEGIN
    INSERT INTO author (name, bio) VALUES (in_name, in_bio) RETURNING id INTO new_id;
    INSERT INTO artist (authorid, image) VALUES (new_id, bytea_import(path_image));
    RETURN FOUND;
  END;
  $$ LANGUAGE plpgsql;
  
CREATE FUNCTION insert_new_group(in_name VARCHAR(75), in_bio TEXT) RETURNS BOOLEAN AS
  $$
  DECLARE
    new_id INT;
  BEGIN
    INSERT INTO author (name, bio) VALUES (in_name, in_bio) RETURNING id INTO new_id;
    INSERT INTO "group" (authorid) VALUES (new_id);
    RETURN FOUND;
  END;
  $$ LANGUAGE plpgsql;
  
create function add_artist_to_group (artist INT, grup INT) RETURNS BOOLEAN AS
  $$

  BEGIN
    INSERT INTO component (groupid, artistid) VALUES (artist, grup);
    RETURN FOUND;
  END;
  $$ LANGUAGE plpgsql;

CREATE FUNCTION insert_new_album(in_name VARCHAR(75), in_date DATE, in_author INT, in_desc TEXT, path_image TEXT) RETURNS BOOLEAN AS
  $$
  BEGIN
    INSERT INTO album (name, publishdate, authorid, description, image) VALUES (in_name, in_date, in_author, in_desc, bytea_import(path_image));
    RETURN FOUND;
  END;
  $$ LANGUAGE plpgsql;

create function bytea_import(p_path text, p_result out bytea) as 
 $$
	declare
  	l_oid oid;
	begin
  		select lo_import(p_path) into l_oid;
  		select lo_get(l_oid) INTO p_result;
  		perform lo_unlink(l_oid);
	end;
$$ language plpgsql;

CREATE FUNCTION insert_new_song(in_name VARCHAR(75), path_file text, in_len INT, in_album INT, in_genre VARCHAR(75)) RETURNS BOOLEAN AS
  $$
  DECLARE
    new_id INT;
  BEGIN
    INSERT INTO song (name, file, lenght, albumid) VALUES (in_name, bytea_import(path_file), in_len, in_album) RETURNING id INTO new_id;
    INSERT INTO genre (name, songid) VALUES (in_genre, new_id);
    RETURN FOUND;
  end;
  $$ LANGUAGE plpgsql;

create type song_info as
(
  id       integer,
  name 	  varchar(75),
  lenght   integer,
  albumid  integer,
  genre    VARCHAR(75)
);

CREATE OR REPLACE FUNCTION get_songs_of_album(in_id INT) RETURNS SETOF song_info AS
  $$
    SELECT s.id, s.name, s.lenght, s.albumid, g.name FROM song s, genre g WHERE albumid = $1 and s.id = g.songid;
  $$ LANGUAGE sql;
  
  
CREATE OR REPLACE FUNCTION get_author_by_id(in_id INT) RETURNS author AS
  $$
  SELECT * FROM author where id = in_id;
  $$ LANGUAGE sql;
  
CREATE OR REPLACE FUNCTION  get_songinfo_by_id(in_id INT) RETURNS song_info AS
  $$
  SELECT s.id, s.name, s.lenght, s.albumid, g.name FROM song s, genre g WHERE s.id = in_id AND s.id = g.songid;
  $$ LANGUAGE sql;
  
CREATE OR REPLACE FUNCTION search_songs_by_name (in_name VARCHAR(75)) RETURNS SETOF song_info AS
  $$
    SELECT s.id, s.name, s.lenght, s.albumid, g.name
    FROM song s, genre g
    WHERE s.id = g.songid AND s.name ILIKE '%' || in_name || '%'
  $$ LANGUAGE sql;

CREATE OR REPLACE FUNCTION search_songs_by_author (in_name VARCHAR(75)) RETURNS SETOF song_info AS
  $$
    SELECT s.id, s.name, s.lenght, s.albumid, g.name
    FROM song s, genre g, album a, author au
    WHERE s.id = g.songid AND s.albumid = a.id AND a.authorid = au.id AND au.name ILIKE '%' || in_name || '%'
  $$ LANGUAGE sql;

CREATE OR REPLACE FUNCTION search_songs_by_genre (in_genre VARCHAR(75)) RETURNS SETOF song_info AS
  $$
    SELECT s.id, s.name, s.lenght, s.albumid, g.name
    FROM song s, genre g
    WHERE s.id = g.songid AND g.name ILIKE '%' || in_genre || '%'
  $$ LANGUAGE sql;
  
CREATE OR REPLACE FUNCTION search_songs(in_name VARCHAR(75), in_auth VARCHAR(75), in_genre VARCHAR(75), in_lim INT, in_off INT) RETURNS SETOF song_info AS
  $$
    SELECT * FROM (
        select * from search_songs_by_name(in_name)
      UNION
        select * from search_songs_by_genre(in_genre)
      UNION
        SELECT * FROM search_songs_by_author(in_auth)
    ) AS song_info
    LIMIT in_lim
    OFFSET in_off;
  $$ LANGUAGE sql;  

CREATE OR REPLACE FUNCTION get_songs_of_list(in_list INT) RETURNS SETOF song_info AS
  $$
  SELECT s.id, s.name, s.lenght, s.albumid, g.name
    FROM song s, genre g, listsong ls, list l
    WHERE s.id = g.songid AND s.id = ls.songid AND ls.listid = l.id AND l.id = in_list
  $$ LANGUAGE sql;

CREATE OR REPLACE FUNCTION search_users(in_name VARCHAR(75), in_username VARCHAR(75), in_lim INT, in_off INT) RETURNS SETOF user_public_info AS
  $$
  SELECT * FROM (
      SELECT id, username, name, bio
      FROM "User"
      WHERE name ILIKE '%' || in_name || '%'
    UNION
      SELECT id, username, name, bio
      FROM "User"
      WHERE username ILIKE '%' || in_username || '%'
  ) as user_public_info
  LIMIT in_lim
  OFFSET in_off
  $$ LANGUAGE sql;

CREATE OR REPLACE FUNCTION search_lists(in_name VARCHAR(75), in_owner VARCHAR(75), in_lim INT, in_off INT) RETURNS SETOF list AS
  $$
  SELECT * FROM (
      SELECT *
      FROM list
      WHERE name ILIKE '%' || in_name || '%'
    UNION
      SELECT l.*
      FROM list l, "User" u
      WHERE l.userid = u.id
            AND (u.username ILIKE '%' || in_owner || '%'
            OR u.name ILIKE '%' || in_owner || '%')
  ) as list
  LIMIT in_lim
  OFFSET in_off
  $$ LANGUAGE sql;

CREATE OR REPLACE FUNCTION get_userinfo_by_id(in_id INT) RETURNs user_public_info AS
  $$
  SELECT id, username, name, bio FROM "User" WHERE id = in_id;
  $$ LANGUAGE sql;

CREATE OR REPLACE FUNCTION search_author(in_name VARCHAR(75), in_lim INT, in_off INT) RETURNS SETOF author AS
  $$
  SELECT *
  FROM author
  WHERE name ILIKE '%' || in_name || '%'
  LIMIT in_lim
  OFFSET in_off
  $$ LANGUAGE sql;
  
CREATE OR REPLACE FUNCTION get_songs_of_album(in_id INT) RETURNS SETOF song_info AS
  $$
    SELECT s.id, s.name, s.lenght, s.albumid, g.name FROM song s, genre g WHERE albumid = $1 and s.id = g.songid;
  $$ LANGUAGE sql;
  
CREATE OR REPLACE FUNCTION search_album(in_name VARCHAR(75), in_auth VARCHAR(75), in_lim INT, in_off INT) RETURNS SETOF album AS
  $$
  SELECT * FROM (
      SELECT *
      FROM album
      WHERE name ILIKE '%' || in_name || '%'
    UNION
      SELECT a.*
      FROM album a, author au
      WHERE a.authorid = au.id AND au.name ILIKE '%' || in_auth || '%'
  ) as album
  LIMIT in_lim
  OFFSET in_off
  $$ language sql;
  






