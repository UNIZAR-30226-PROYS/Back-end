CREATE TABLE "User"
(
  id       SERIAL       NOT NULL,
  username VARCHAR(75)  NOT NULL,
  email    VARCHAR(75)  NOT NULL,
  name     VARCHAR(200),
  bio      TEXT,
  password VARCHAR(200) NOT NULL,
  admin    boolean default false not null,
  CONSTRAINT "User_pkey"
  PRIMARY KEY (id)
);

CREATE UNIQUE INDEX user_username_uindex
  ON "User" (username);

CREATE UNIQUE INDEX user_email_uindex
  ON "User" (email);

CREATE TABLE list
(
  id           SERIAL      NOT NULL,
  name         VARCHAR(75) NOT NULL,
  userid       INTEGER     NOT NULL,
  creationdate DATE        NOT NULL,
  description  TEXT,
  isfav        boolean default false not null,
  CONSTRAINT list_pkey
  PRIMARY KEY (id),
  CONSTRAINT list_user_id_fk
  FOREIGN KEY (userid) REFERENCES "User"
);

CREATE TABLE author
(
  id   SERIAL      NOT NULL,
  name VARCHAR(75) NOT NULL,
  bio  TEXT,
  CONSTRAINT author_pkey
  PRIMARY KEY (id)
);

CREATE TABLE artist
(
  authorid INTEGER NOT NULL,
  image    BYTEA,
  CONSTRAINT artist_pkey
  PRIMARY KEY (authorid),
  CONSTRAINT artist_author_id_fk
  FOREIGN KEY (authorid) REFERENCES author
);

CREATE TABLE "group"
(
  authorid INTEGER NOT NULL,
  CONSTRAINT group_pkey
  PRIMARY KEY (authorid),
  CONSTRAINT group_author_id_fk
  FOREIGN KEY (authorid) REFERENCES author
);

CREATE TABLE component
(
  groupid  INTEGER NOT NULL,
  artistid INTEGER NOT NULL,
  CONSTRAINT component_groupid_artistid_pk
  PRIMARY KEY (groupid, artistid),
  CONSTRAINT component_group_authorid_fk
  FOREIGN KEY (groupid) REFERENCES "group",
  CONSTRAINT component_artist_authorid_fk
  FOREIGN KEY (artistid) REFERENCES artist
);

CREATE TABLE song
(
  id      SERIAL      NOT NULL,
  name    VARCHAR(75) NOT NULL,
  file    BYTEA       NOT NULL,
  lenght  INTEGER     NOT NULL,
  albumid INTEGER,
  CONSTRAINT song_pkey
  PRIMARY KEY (id)
);

CREATE TABLE listsong
(
  listid INTEGER NOT NULL,
  songid INTEGER NOT NULL,
  CONSTRAINT listsong_listid_songid_pk
  PRIMARY KEY (listid, songid),
  CONSTRAINT listsong_list_id_fk
  FOREIGN KEY (listid) REFERENCES list,
  CONSTRAINT listsong_song_id_fk
  FOREIGN KEY (songid) REFERENCES song
);

CREATE TABLE album
(
  id          SERIAL      NOT NULL,
  name        VARCHAR(75) NOT NULL,
  publishdate DATE,
  authorid    INTEGER     NOT NULL,
  description TEXT,
  image       BYTEA,
  CONSTRAINT album_pkey
  PRIMARY KEY (id),
  CONSTRAINT album_author_id_fk
  FOREIGN KEY (authorid) REFERENCES author
);

ALTER TABLE song
  ADD CONSTRAINT song_album_id_fk
FOREIGN KEY (albumid) REFERENCES album;

CREATE TABLE genre
(
  name   VARCHAR(75) NOT NULL,
  songid INTEGER     NOT NULL,
  CONSTRAINT genre_name_songid_pk
  PRIMARY KEY (name, songid),
  CONSTRAINT genre_song_id_fk
  FOREIGN KEY (songid) REFERENCES song
);

CREATE TABLE follower
(
  userid     INTEGER NOT NULL,
  followedid INTEGER NOT NULL,
  CONSTRAINT follower_userid_followedid_pk
  PRIMARY KEY (userid, followedid),
  CONSTRAINT follower__fk_uid
  FOREIGN KEY (userid) REFERENCES "User",
  CONSTRAINT follower__fk_fid
  FOREIGN KEY (followedid) REFERENCES "User"
);

create table usersession
(
  id     serial  not null,
  userid integer not null,
  listid integer,
  songid integer,
  time   integer,
  constraint usersession_pkey
  primary key (id),
  constraint usersession_user_id_fk
  foreign key (userid) references "User",
  constraint usersession_listsong_listid_songid_fk
  foreign key (listid, songid) references listsong
);

create unique index usersession_userid_uindex
  on usersession (userid);

-- ROLES --
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
