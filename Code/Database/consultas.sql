--usuario dado su identificador
SELECT get_user_by_id(id INT); -- RETURNS full user

--Lista de usuarios que sigue el usuario dado
SELECT get_followed_by_user(id INT, limit INT, offset INT); --RETURNS id, nick, name, bio

--Lista de usuarios que siguen a un usuario dado
SELECT get_followers_by_user(id INT, limit INT, offset INT);  --RETURNS id, nick, name, bio

--Listas de playLists de un usuario dado
SELECT get_list_by_ownerid(id INT, limit INT, offset INT); -- RETURNS full list info

--Lista de playLists dado su id
SELECT get_list_by_id(id INT); --retuns 1 list item info

--Obtener albunes dado año de lanzamiento
SELECT get_album_by_publish_year(year INT, limit INT, offset INT);

-- Obtener albunes dado un nombre. name must gone 'text'
SELECT get_album_by_name(name VARCHAR(75), limit INT, offset INT);

-- Obtener el nombre de un autor dado su id
SELECT get_author_name_by_id(id INT); -- RETURNS VARCHAR(75)

--Lista de autores dado el nombre
SELECT get_authors_by_name(name VARCHAR(75), limit INT, offset INT);

-- Lista de usuarios dado parametros
SELECT get_users_by_parameter(searchquery VARCHAR(75), limit INT, offset INT);


--Objener imagen de un album dado su identificador
SELECT image FROM album WHERE id = ?;

--Obtener imagen de una cancion dado su identificador
SELECT a.image FROM album a, song s WHERE a.id = s.albumid AND s.id = ?;

-- Obtener fichero de audio de una cancion dado un id
SELECT file FROM song WHERE id = ?;

-- Obtener lista de albunes dado un autor
SELECT get_album_by_authorid(id INT, limit INT, offset INT);

--Lista de canciones de una playList
SELECT c.id, c.name, c.genre, c.file, c.lenght, c.groupid, c.albumid FROM song c, list l, listsong ls WHERE c.id = ls.songid AND ls.listid = l.id AND l.id = ? LIMIT ? OFFSET ?;

--Lista de canciones dado un genero. Genero debe ir '%genero%'
SELECT id, name, genre, file, lenght, groupid, albumid FROM song WHERE genre LIKE ? LIMIT ? OFFSET ?;

--Lista de canciones dado el id de un autor
SELECT c.id, c.name, c.genre, c.file, c.lenght, c.groupid, c.albumid
FROM song c, "Group" g, components cp, artist a
WHERE c.groupid = g.id AND g.id = cp.groupid AND cp.artistid = a.id AND a.id = ? LIMIT ? OFFSET ?;

--Lista de canciones dado un identificador de grupo
SELECT c.id, c.name, c.genre, c.file, c.lenght, c.groupid, c.albumid
FROM song c, "Group" g, components cp, artist a
WHERE c.groupid = g.id AND g.id = ? LIMIT ? OFFSET ?;








-- Insertar nueva lista
SELECT insert_new_play_list(name VARCHAR(75), userid INT, description TEXT); -- returns true or false if execute

-- Insertar nuevo usuario y crea su lista de favoritos automaticamente
SELECT insert_new_user(username VARCHAR(75), email VARCHAR(75), name VARCHAR(200), password VARCHAR(200)); -- RETURNS TRUE or false if execute

-- Seguir a un usuario
SELECT follow_user(actual INT, seguido INT); -- RETURNS TRUE OR FALSE if execute

-- Añadir cancion a una lista
SELECT insert_song_in_list(list INT, song INT) --RETURN TRUE OR FALSE of execute









