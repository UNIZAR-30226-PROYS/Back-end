import connexion
import six

from swagger_server.models.album_item import AlbumItem  # noqa: E501
from swagger_server.models.album_item_new import AlbumItemNew  # noqa: E501
from swagger_server.models.song_item import SongItem  # noqa: E501
from swagger_server.models.song_item_new import SongItemNew  # noqa: E501
from swagger_server import util

import swagger_server.controllers.public_controller as public

from flask import session, Response
from swagger_server.database import engine
import swagger_server.authentificator as auth


@auth.enforce_auth
@auth.enforce_admin
def add_album(albumItem=None):  # noqa: E501
    """crea un álbum

    Un administrador crea un álbum # noqa: E501

    :param albumItem: Album item to add
    :type albumItem: dict | bytes

    :rtype: AlbumItem
    """
    if connexion.request.is_json:
        albumItem = AlbumItemNew.from_dict(connexion.request.get_json())  # noqa: E501

    connection = engine.connect()
    trans = connection.begin()

    sql = "SELECT * FROM insert_new_album( '{}', '{}', {} , '{}', '{}') AS id;" \
        .format(albumItem.name, albumItem.publish_date, albumItem.author_id, albumItem.description, '0x00')
    query = connection.execute(sql)
    trans.commit()
    connection.close()

    id = query.first()['id']

    return public.get_album(id)


@auth.enforce_auth
@auth.enforce_admin
def add_album_song(albumID, songID=None):  # noqa: E501
    """añade una canción a un album

    Un admin añade una canción a un album # noqa: E501

    :param albumID: ID del album
    :type albumID: str
    :param songID: Song to add
    :type songID: str

    :rtype: AlbumItem
    """
    return 'do some magic!'


@auth.enforce_auth
@auth.enforce_admin
def add_song(songItem=None):  # noqa: E501
    """añade una canción

    Un admin añade una canción a la base de datos. # noqa: E501

    :param songItem: Song item to add
    :type songItem: dict | bytes

    :rtype: SongItem
    """
    if connexion.request.is_json:
        songItem = SongItemNew.from_dict(connexion.request.get_json())  # noqa: E501

    connection = engine.connect()
    trans = connection.begin()

    sql = "SELECT * FROM insert_new_song( '{}', '{}', {} , {}, '{}') AS id;"\
        .format(songItem.name, '0x00', songItem.lenght, songItem.album_id, songItem.genre[0])
    query = connection.execute(sql)
    trans.commit()
    connection.close()

    id = query.first()['id']

    return public.get_song(id)


@auth.enforce_auth
@auth.enforce_admin
def delete_album(albumID):  # noqa: E501
    """elimina un álbum

    Elimina el álbum identificado por albumID  # noqa: E501

    :param albumID: ID del álbum
    :type albumID: str

    :rtype: None
    """
    return 'do some magic!'


@auth.enforce_auth
@auth.enforce_admin
def delete_album_image(albumID):  # noqa: E501
    """elimina la carátula de un álbum

    Elimina la carátula de un álbum identificadoa por albumID  # noqa: E501

    :param albumID: ID del álbum
    :type albumID: str

    :rtype: None
    """
    connection = engine.connect()
    trans = connection.begin()


    sql = "SELECT * FROM update_album_image( {}, '{}') AS insertado;" \
        .format(albumID, '0x00')
    query = connection.execute(sql)
    trans.commit()
    connection.close()

    if not query.first()['insertado']:
        return 'Not found', 404


@auth.enforce_auth
@auth.enforce_admin
def delete_author_image(authorID):  # noqa: E501
    """elimina la imagen de un autor

    Elimina la imagen de un autor identificado por authorID  # noqa: E501

    :param authorID: ID del autor
    :type authorID: str

    :rtype: None
    """
    return 'do some magic!'


@auth.enforce_auth
@auth.enforce_admin
def delete_song(songID):  # noqa: E501
    """elimina una canción

    Elimina información y fichero de  la canción identificada por songID  # noqa: E501

    :param songID: ID de la canción
    :type songID: str

    :rtype: None
    """
    return 'do some magic!'


@auth.enforce_auth
@auth.enforce_admin
def delete_song_file(songID):  # noqa: E501
    """elimina el archivo de audio de una canción

    Elimina el fichero de audio de una canción identificada por songID  # noqa: E501

    :param songID: ID de la canción
    :type songID: str

    :rtype: None
    """
    connection = engine.connect()
    trans = connection.begin()

    sql = "SELECT * FROM update_song_file( {}, '{}') AS insertado;" \
        .format(songID, '0x00')
    query = connection.execute(sql)
    trans.commit()
    connection.close()

    if not query.first()['insertado']:
        return 'Not found', 404


@auth.enforce_auth
@auth.enforce_admin
def delete_song_image(songID):  # noqa: E501
    """elimina la carátula de una canción

    Elimina la carátula de una canción identificada por songID  # noqa: E501

    :param songID: ID de la canción
    :type songID: str

    :rtype: None
    """
    return 'do some magic!'


@auth.enforce_auth
@auth.enforce_admin
def update_song(songID, songItem=None):  # noqa: E501
    """actualiza la información de una canción

    Un admin actualiza la información de una canción. # noqa: E501

    :param songID: ID de la canción
    :type songID: str
    :param songItem: Song item to update
    :type songItem: dict | bytes

    :rtype: SongItem
    """
    if connexion.request.is_json:
        songItem = SongItemNew.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


@auth.enforce_auth
@auth.enforce_admin
def upload_album_image(albumID, albumImage):  # noqa: E501
    """carga la carátula de un álbum

    Un admin carga la carátula de un álbum con identificador albumID. # noqa: E501

    :param albumID: ID del álbum
    :type albumID: str
    :param albumImage: Album image to update
    :type albumImage: werkzeug.datastructures.FileStorage

    :rtype: None
    """
    connection = engine.connect()
    trans = connection.begin()

    fichero = albumImage.read()

    sql = "SELECT * FROM update_album_image( {}, %s) AS insertado;" \
        .format(albumID)
    query = connection.execute(sql, (fichero))
    trans.commit()
    connection.close()

    if not query.first()['insertado']:
        return 'Not found', 404


@auth.enforce_auth
@auth.enforce_admin
def upload_author_image(authorID, authorImage):  # noqa: E501
    """carga la imagen e un autor

    Un admin carga la imagen de un autor con identificador authorID. # noqa: E501

    :param authorID: ID del autor
    :type authorID: str
    :param authorImage: Image item to update
    :type authorImage: werkzeug.datastructures.FileStorage

    :rtype: None
    """
    return 'do some magic!'


@auth.enforce_auth
@auth.enforce_admin
def upload_song_file(songID, songFile):  # noqa: E501
    """carga el archivo de audio de una canción

    Un admin carga el archivo de audio de una canción con identificador songID. # noqa: E501

    :param songID: ID de la canción
    :type songID: str
    :param songFile: Song item to update
    :type songFile: werkzeug.datastructures.FileStorage

    :rtype: None
    """
    connection = engine.connect()
    trans = connection.begin()

    fichero = songFile.read()

    sql = "SELECT * FROM update_song_file( {}, %s) AS insertado;" \
        .format(songID)
    query = connection.execute(sql, (fichero))
    trans.commit()
    connection.close()

    if not query.first()['insertado']:
        return 'Not found', 404


@auth.enforce_auth
@auth.enforce_admin
def upload_song_image(songID, songImage):  # noqa: E501
    """carga la carátula de una canción

    Un admin carga la carátula de una canción con identificador songID. # noqa: E501

    :param songID: ID de la canción
    :type songID: str
    :param songImage: Image item to update
    :type songImage: werkzeug.datastructures.FileStorage

    :rtype: None
    """
    return 'do some magic!'
