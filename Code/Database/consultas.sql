--usuario dado su identificador
SELECT id, username, email, name, bio, password FROM "User" WHERE id = ?;
--// Esta consultas es lo mismo que SELECT * FROM "User" WHERE id = ?;
--// pero te la pongo asi por si tuvieras que sacar solo un parametro

--Lista de usuarios que sigue el usuario dado
SELECT u.id, u.username, u.email, u.name, u.bio, u.password FROM "User" u, follower f WHERE u.id = f.followedid AND f.userid = ?;

--Lista de usuarios que siguen a un usuario dado
SELECT u.id, u.username, u.email, u.name, u.bio, u.password FROM "User" u, follower f WHERE u.id = f.userid AND f.followedid = ?;

--Lista de playLists de un usuario dado
SELECT id, name, userid, creationdate, description FROM list WHERE userid = ?;

--Objener imagen de un album dado su identificador
SELECT image FROM album WHERE id = ?;

-- Obtener fichero de audio de una cancion dado un id
SELECT file FROM song WHERE id = ?;

--Obtener albunes dado año de lanzamiento
SELECT * FROM album WHERE EXTRACT(YEAR FROM publishdate) = ?;

-- Obtener lista de albunes dado un autor
SELECT a.id, a.name, a.groupid, a.publishdate, a.description, a.image FROM album a, components c, "Group" g WHERE a.groupid = g.id AND g.id = c.groupid AND c.artistid = ?;

--Lista de canciones de una playList
SELECT c.id, c.name, c.file, c.lenght, c.groupid, c.albumid FROM song c, list l, listsong ls WHERE c.id = ls.songid AND ls.listid = l.id AND l.id = ?;