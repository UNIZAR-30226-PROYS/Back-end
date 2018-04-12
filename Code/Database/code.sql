CREATE TABLE public."User"
(
				id SERIAL PRIMARY KEY,
    username VARCHAR(75) NOT NULL,
    email VARCHAR(75) NOT NULL,
    name VARCHAR(200),
    bio TEXT,
    password VARCHAR(200) NOT NULL
);
CREATE UNIQUE INDEX User_email_uindex ON public."User" (email);
CREATE UNIQUE INDEX User_username_uindex ON public."User" (username);

CREATE TABLE public.Follower
(
    userID INT NOT NULL,
    followedID INT NOT NULL,
    CONSTRAINT follower_userid_followedid_pk PRIMARY KEY (userid, followedid),
    CONSTRAINT Follower__fk_uid FOREIGN KEY (userID) REFERENCES "User" (id),
    CONSTRAINT Follower__fk_fid FOREIGN KEY (followedID) REFERENCES "User" (id)
);

CREATE TABLE public.List
(
    id SERIAL PRIMARY KEY,
    name VARCHAR(75) NOT NULL,
    userid INT NOT NULL,
    creationdate DATE NOT NULL,
    description TEXT NULL,
    CONSTRAINT List_User_id_fk FOREIGN KEY (userid) REFERENCES "User" (id)
);

CREATE TABLE public."Group"
(
    id SERIAL PRIMARY KEY,
    name VARCHAR(75) NOT NULL,
    bio TEXT
);

CREATE TABLE public.Album
(
    id SERIAL PRIMARY KEY,
    name VARCHAR(75) NOT NULL,
    groupid INT NOT NULL,
    publishDate DATE NOT NULL,
    description TEXT,
    image BYTEA NOT NULL,
    CONSTRAINT Album_Group_id_fk FOREIGN KEY (groupid) REFERENCES "Group" (id)
);

CREATE TABLE public.Song
(
    id SERIAL PRIMARY KEY,
    name VARCHAR(75) NOT NULL,
    genre VARCHAR(75) NOT NULL,
    file BYTEA NOT NULL,
    lenght INT,
    groupID INT NOT NULL,
    albumID INT NOT NULL,
    CONSTRAINT Song_Group_id_fk FOREIGN KEY (groupID) REFERENCES "Group" (id),
    CONSTRAINT Song_album_id_fk FOREIGN KEY (albumID) REFERENCES album (id)
);

CREATE TABLE public.Artist
(
    id SERIAL PRIMARY KEY,
    name VARCHAR(75) NOT NULL,
    bio TEXT
);

CREATE TABLE public.listSong
(
    listID INT NOT NULL,
    songID INT NOT NULL,
    CONSTRAINT listSong_listID_songID_pk PRIMARY KEY (listID, songID),
    CONSTRAINT listSong_list_id_fk FOREIGN KEY (listID) REFERENCES list (id),
    CONSTRAINT listSong_song_id_fk FOREIGN KEY (songID) REFERENCES song (id)
);

CREATE TABLE public.Components
(
    GroupID INT NOT NULL,
    ArtistID INT NOT NULL,
    CONSTRAINT Components_GroupID_ArtistID_pk PRIMARY KEY (GroupID, ArtistID),
    CONSTRAINT Components_Group_id_fk FOREIGN KEY (GroupID) REFERENCES "Group" (id),
    CONSTRAINT Components_artist_id_fk FOREIGN KEY (ArtistID) REFERENCES artist (id)
);

CREATE TABLE public.Session
(
    id SERIAL PRIMARY KEY,
    userid INT NOT NULL,
    listid INT NOT NULL,
    songid INT NOT NULL,
    time INT NOT NULL,
    CONSTRAINT Session_listsong_listid_songid_fk FOREIGN KEY (listid, songid) REFERENCES listsong (listid, songid)
);

-- Creado el rol de escritura y lectura
CREATE ROLE read_write LOGIN PASSWORD 'PasswordReadWrite';

-- Leer tablas en schema public
GRANT SELECT ON ALL TABLES IN SCHEMA public to read_write;

-- Leer futuras tablas en schema public
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT ON TABLES TO read_write;

-- Insertar en tablas en schema public
GRANT INSERT ON ALL TABLES IN SCHEMA public to read_write;

-- Insertar en futuras tablas en schema public
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT INSERT ON TABLES TO read_write;

-- Eliminar en tablas en schema public
GRANT DELETE ON ALL TABLES IN SCHEMA public to read_write;

-- Eliminar en futuras tablas en schema public
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT DELETE ON TABLES TO read_write;

-- Actualizar en tablas en schema public
GRANT UPDATE ON ALL TABLES IN SCHEMA public to read_write;

-- Actualizar en futuras tablas en schema public
ALTER DEFAULT PRIVILEGES  IN SCHEMA public
    GRANT UPDATE ON TABLES TO read_write;
