CREATE FUNCTION get_user_by_id(id INT) RETURNS "User" AS
  $$
    SELECT * FROM "User" WHERE id = $1;
  $$ LANGUAGE sql;

CREATE FUNCTION get_user_by_username(username VARCHAR(75)) RETURNS "User" AS
  $$
    SELECT * FROM "User" WHERE username = $1;
  $$ LANGUAGE sql;


CREATE FUNCTION get_user_by_mail(mail VARCHAR(75)) RETURNS "User" AS
  $$
    SELECT * FROM "User" WHERE email = $1;
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
  
create or replace function insert_new_play_list(name character varying, userid integer, bio text)
  returns integer
language plpgsql
as $$
DECLARE
    new_id INT;
BEGIN
    IF userid IN (SELECT id FROM "User") THEN
      INSERT INTO list (name, userid, creationdate, description)
      VALUES ($1,$2,current_date,$3) RETURNING id INTO new_id;
      RETURN new_id;
    ELSE
      RETURN null;
    END IF;
  END;
$$;
  
create function insert_fav_play_list(name character varying, userid integer, bio text)
  returns boolean
language plpgsql
as $$
BEGIN
    IF userid IN (SELECT id FROM "User") THEN
      INSERT INTO list (name, userid, creationdate, description, isfav)
      VALUES ($1,$2,current_date,$3, TRUE);
      RETURN FOUND;
    ELSE
      RETURN FALSE;
    END IF;
  END;
$$;
  
CREATE FUNCTION insert_new_user(username VARCHAR(75), mail VARCHAR(75), name VARCHAR(200), password VARCHAR(200)) RETURNS BOOLEAN AS
  $$
  DECLARE
    new_id INT;
  BEGIN
    IF mail NOT IN (SELECT u.email FROM "User" u) THEN
      INSERT INTO "User" (username, email, name, password)
      VALUES ($1, $2, $3, $4)
      RETURNING id INTO new_id;
      INSERT INTO usersession (userid) VALUES (new_id);
      RETURN insert_fav_play_list('Favoritos', new_id, 'Tu música favorita');
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
  
CREATE FUNCTION insert_new_artist(in_name VARCHAR(75), in_bio TEXT, image bytea) RETURNS BOOLEAN AS
  $$
  DECLARE
    new_id INT;
  BEGIN
    INSERT INTO author (name, bio) VALUES (in_name, in_bio) RETURNING id INTO new_id;
    INSERT INTO artist (authorid, image) VALUES (new_id, image);
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

CREATE FUNCTION insert_new_album(in_name VARCHAR(75), in_date DATE, in_author INT, in_desc TEXT, image bytea) RETURNS BOOLEAN AS
  $$
  BEGIN
    INSERT INTO album (name, publishdate, authorid, description, image) VALUES (in_name, in_date, in_author, in_desc, image);
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

CREATE FUNCTION insert_new_song(in_name VARCHAR(75), file bytea, in_len INT, in_album INT, in_genre VARCHAR(75)) RETURNS BOOLEAN AS
  $$
  DECLARE
    new_id INT;
  BEGIN
    INSERT INTO song (name, file, lenght, albumid) VALUES (in_name, file, in_len, in_album) RETURNING id INTO new_id;
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
  
  CREATE OR REPLACE FUNCTION search_listsAnd(in_name VARCHAR(75), in_owner VARCHAR(75), in_lim INT, in_off INT) RETURNS SETOF list AS
  $$
  SELECT l.*
	FROM list l, "User" u
	WHERE l.name ILIKE '%' || in_name || '%'
      AND l.userid = u.id
      AND (u.username ILIKE '%' || in_owner || '%'
            OR u.name ILIKE '%' || in_owner || '%')
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

CREATE OR REPLACE FUNCTION check_list_user(in_user INT, in_list INT) RETURNS BIGINT AS
  $$
  SELECT COUNT(id)
  FROM list
  WHERE userid = in_user AND id = in_list
  $$ language sql;

create function unfollow_user(actual integer, unfollowed integer) returns boolean as $$
BEGIN
    IF (actual IN (SELECT id FROM "User")) AND (unfollowed IN (SELECT id FROM "User")) THEN
      IF actual IN (SELECT userid FROM follower WHERE userid = actual AND followedid = unfollowed) THEN
        DELETE FROM follower WHERE userid = actual AND followedid = unfollowed;
        RETURN FOUND;
      ELSE
        RETURN FALSE;
      END IF;
    ELSE
      RETURN FALSE;
    END IF;
  END;
$$ language plpgsql;

create or replace function del_list_song(in_list INT, in_song INT) RETURNS BOOLEAN AS
  $$
  BEGIN
    DELETE FROM listsong WHERE listid = in_list AND songid = in_song;
    RETURN FOUND;
  end;
  $$ LANGUAGE plpgsql;

create or replace function del_list(in_list INT) RETURNS BOOLEAN AS
  $$
  BEGIN
    IF (SELECT isfav FROM list WHERE id = in_list) = TRUE THEN
      RETURN FALSE;
    ELSE
      DELETE FROM listsong WHERE listid = in_list;
      DELETE FROM list WHERE id = in_list;
      RETURN FOUND;
    end if;
  end;
  $$ LANGUAGE plpgsql;

CREATE OR REPLACE function del_user(in_id INT) RETURNS BOOLEAN AS
  $$
  BEGIN
    DELETE FROM usersession WHERE userid = in_id;
    DELETE FROM listsong WHERE listid IN (SELECT id FROM list WHERE userid = in_id);
    DELETE FROM list WHERE userid = in_id;
    DELETE FROM follower WHERE userid = in_id OR followedid = in_id;
    DELETE FROM "User" WHERE id = in_id;
    RETURN FOUND;
  end;
  $$ LANGUAGE plpgsql;
  
CREATE OR REPLACE FUNCTION get_session(in_userid INT) RETURNS usersession AS
  $$
  SELECT * FROM usersession WHERE userid = in_userid;
  $$ LANGUAGE sql;

CREATE OR REPLACE FUNCTION update_list(in_list INT, in_name varchar(75), in_desc text) RETURNS BOOLEAN AS
  $$
  BEGIN
    IF (SELECT isfav FROM list WHERE id = in_list) = TRUE THEN
      RETURN FALSE;
    ELSE
      UPDATE list set name = in_name, description = in_desc WHERE id = in_list;
      RETURN FOUND;
    end if;
  end;
  $$ LANGUAGE plpgsql;
  
CREATE OR REPLACE FUNCTION update_song_file(songid INT, in_file bytea) RETURNS BOOLEAN AS
  $$
  BEGIN
    UPDATE song set file = in_file WHERE id = songid;
    RETURN FOUND;
  end;
  $$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION search_one_list(in_owner int, in_text text, in_name VARCHAR(75)) RETURNS INTEGER AS
  $$
    SELECT id
    FROM list
    WHERE description = in_text AND name = in_name AND userid = in_owner
    ORDER BY creationdate DESC
    LIMIT 1;
  $$ LANGUAGE sql;

CREATE OR REPLACE FUNCTION update_user(in_id INT, in_bio TEXT, in_name VARCHAR(200), in_user VARCHAR(75)) RETURNS BOOLEAN AS
  $$
  BEGIN
    UPDATE "User" SET bio = in_bio, name = in_name, username = in_user WHERE id = in_id;
    RETURN FOUND;
  end;
  $$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_user_credentials(in_id INT, in_email VARCHAR(75), in_pass VARCHAR(200)) RETURNS BOOLEAN AS
  $$
  BEGIN
    UPDATE "User" SET email = in_email, password = in_pass WHERE id = in_id;
    RETURN FOUND;
  END;
  $$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_user_session(in_id INT, in_list INT, in_song INT, in_time INT) RETURNS BOOLEAN AS
  $$
  BEGIN
    UPDATE usersession SET listid = in_list, songid = in_song, time = in_time WHERE userid = in_id;
    RETURN FOUND;
  end;
  $$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION make_admin(in_id INT) RETURNS BOOLEAN AS
  $$
  BEGIN
    UPDATE "User" SET admin = TRUE WHERE id = in_id;
    RETURN FOUND;
  end;
  $$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION search_usersAnd(in_name VARCHAR(75), in_username VARCHAR(75), in_lim INT, in_off INT) RETURNS SETOF user_public_info AS
  $$
  SELECT id, username, name, bio
  FROM "User"
  WHERE name ILIKE '%' || in_name || '%' AND username  ILIKE '%' || in_username || '%'
  LIMIT in_lim
  OFFSET in_off
  $$ LANGUAGE sql;
  
create function search_songsAnd(in_name character varying, in_auth character varying, in_genre character varying, in_lim integer, in_off integer)
  returns SETOF song_info
language sql
as $$
SELECT s.id, s.name, s.lenght, s.albumid, g.name
    FROM song s, genre g, album a, author au
    WHERE s.id = g.songid
          AND s.albumid = a.id
          AND a.authorid = au.id
          AND s.name ILIKE '%' || in_name || '%'
          AND au.name ILIKE '%' || in_auth || '%'
          AND g.name ILIKE '%' || in_genre || '%'
    LIMIT in_lim
    OFFSET in_off;
$$;

CREATE OR REPLACE FUNCTION search_albumAnd(in_name VARCHAR(75), in_auth VARCHAR(75), in_lim INT, in_off INT) RETURNS SETOF album AS
  $$
  SELECT a.*
  FROM album a, author au
  WHERE a.name ILIKE '%' || in_name || '%'
        AND a.authorid = au.id
        AND au.name ILIKE '%' || in_auth || '%'
  LIMIT in_lim
  OFFSET in_off
  $$ language sql;
