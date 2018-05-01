import connexion
import six

from swagger_server.models.account_item import AccountItem  # noqa: E501
from swagger_server.models.album_item import AlbumItem  # noqa: E501
from swagger_server.models.author_item import AuthorItem  # noqa: E501
from swagger_server.models.login_item import LoginItem  # noqa: E501
from swagger_server.models.playlist_item import PlaylistItem  # noqa: E501
from swagger_server.models.profile_item import ProfileItem  # noqa: E501
from swagger_server.models.sign_up_item import SignUpItem  # noqa: E501
from swagger_server.models.song_item import SongItem  # noqa: E501
from swagger_server import util

from flask import session
from swagger_server.database import engine
import swagger_server.authentificator as auth


def create_account(signupItem=None):  # noqa: E501
    """crea cuenta de usuario

    Crea una cuenta de usuario # noqa: E501

    :param signupItem: Datos de la nueva cuenta
    :type signupItem: dict | bytes

    :rtype: AccountItem
    """
    if connexion.request.is_json:
        signupItem = SignUpItem.from_dict(connexion.request.get_json())  # noqa: E501

    search = search_profiles(username=signupItem.username)
    if search.__len__() != 0:
        return 'Username used', 400

    sql = "SELECT * FROM insert_new_user( '{}', '{}', '{}' , '{}'); COMMIT;"\
        .format(signupItem.username, signupItem.mail, signupItem.name, signupItem._pass)
    engine.execute(sql)

    search = search_profiles(SignUpItem.name, signupItem.username, 0, 1)
    if search.__len__() == 0:
        return 'Error inserting', 400
    inserted = search[0]

    auth.sign_in(inserted.id)

    return AccountItem(inserted.id, inserted.username, inserted.name, inserted.bio,
                       signupItem.mail, inserted.friends, inserted.playlists)


def get_album(albumID):  # noqa: E501
    """obtiene un álbum

    Obtiene los datos del álbum identificada por albumID  # noqa: E501

    :param albumID: ID del álbum
    :type albumID: str

    :rtype: AlbumItem
    """
    return 'do some magic!'


def get_album_image(albumID):  # noqa: E501
    """obtiene la carátula de un álbum

    Obtiene la carátula de un álbum identificado por albumID  # noqa: E501

    :param albumID: ID del álbum
    :type albumID: str

    :rtype: file
    """
    return 'do some magic!'


def get_author(authorID):  # noqa: E501
    """obtiene un perfil de autor identificado por authorID

    Obtiene un perfil de autor identificado por authorID  # noqa: E501

    :param authorID: ID del autor
    :type authorID: str

    :rtype: AuthorItem
    """

    if authorID == '4678':
        author = AuthorItem('4678','Estopa','Los hermanos Muñóz de Cornellá')
        return author, 200
    else:
        return 'Not found', 404


def get_author_image(authorID):  # noqa: E501
    """obtiene la imagen de un autor

    Obtiene la imagen de un autor identificado por authorID  # noqa: E501

    :param authorID: ID del autor
    :type authorID: str

    :rtype: file
    """
    return 'do some magic!'


def get_playlist(playlistID):  # noqa: E501
    """obtiene una playlist

    Obtiene los datos de la playlist identificada por playlistID  # noqa: E501

    :param playlistID: ID de la playlist
    :type playlistID: str

    :rtype: PlaylistItem
    """
    return 'do some magic!'


def get_profile(profileID):  # noqa: E501
    """obtiene un perfil de usuario identificado por profileID

    Obtiene un perfil de usuario identificado por profileID.  # noqa: E501

    :param profileID: ID del perfil
    :type profileID: str

    :rtype: ProfileItem
    """

    sql = "SELECT * FROM get_user_by_id( {} )".format(profileID)
    query = engine.execute(sql)
    datos = query.first()
    if datos['id'] is None:
        return 'Not found', 404

    return ProfileItem(datos['id'], datos['username'], datos['name'])


def get_song(songID):  # noqa: E501
    """obtiene información de una canción

    Obtiene los datos de la canción identificada por songID  # noqa: E501

    :param songID: ID de la canción
    :type songID: str

    :rtype: SongItem
    """
    return 'do some magic!'


def get_song_file(songID):  # noqa: E501
    """obtiene el archivo de audio de una canción

    Obtiene el archivo de audio de la canción identificada por songID  # noqa: E501

    :param songID: ID de la canción
    :type songID: str

    :rtype: file
    """
    return 'do some magic!'


def get_song_image(songID):  # noqa: E501
    """obtiene la carátula de una canción

    Obtiene la carátula de la canción identificada por songID  # noqa: E501

    :param songID: ID de la canción
    :type songID: str

    :rtype: file
    """
    return 'do some magic!'


def login(loginItem=None):  # noqa: E501
    """inicia sesión de usuario

    Inicia sesión de usuario. El campo \&quot;friends\&quot; de los amigos de un usuario está siempre vacío (valor NULL) # noqa: E501

    :param loginItem: Credenciales
    :type loginItem: dict | bytes

    :rtype: AccountItem
    """
    if connexion.request.is_json:
        loginItem = LoginItem.from_dict(connexion.request.get_json())  # noqa: E501

    sql = "SELECT * FROM get_user_by_mail( '{}' )".format(loginItem.mail)
    query = engine.execute(sql)
    usuario = query.first()
    if usuario['id'] is None:
        return 'Username non existant', 400

    if usuario['password'] != loginItem._pass:
        return 'Wrong authentification', 400

    auth.sign_in(usuario['id'])

    return AccountItem(usuario['id'],usuario['username'],usuario['name'],usuario['bio'],usuario['email'])


def search_album(name=None, author=None, skip=None, limit=None):  # noqa: E501
    """busca álbunes con ciertos parámetros

    Al pasarle ciertos parámetros devuelve álbunes que se ajusten a ellos  # noqa: E501

    :param name: nombre del álbum
    :type name: str
    :param author: autor del álbum
    :type author: str
    :param skip: number of records to skip for pagination
    :type skip: int
    :param limit: maximum number of records to return
    :type limit: int

    :rtype: List[AlbumItem]
    """
    return 'do some magic!'


def search_authors(name=None, skip=None, limit=None):  # noqa: E501
    """busca autores con ciertos parámetros

    Al pasarle ciertos parámetros devuelve autores que se ajusten a ellos  # noqa: E501

    :param name: nombre del autor
    :type name: str
    :param skip: number of records to skip for pagination
    :type skip: int
    :param limit: maximum number of records to return
    :type limit: int

    :rtype: List[AuthorItem]
    """
    return 'do some magic!'


def search_playlist(name=None, owner=None, skip=None, limit=None):  # noqa: E501
    """busca listas de reproducción con ciertos parámetros

    Al pasarle ciertos parámetros devuelve listas de reproducción que se ajusten a ellos  # noqa: E501

    :param name: nombre de la lista
    :type name: str
    :param owner: propietario de la lista
    :type owner: str
    :param skip: number of records to skip for pagination
    :type skip: int
    :param limit: maximum number of records to return
    :type limit: int

    :rtype: List[PlaylistItem]
    """
    return 'do some magic!'


def search_profiles(name='*****', username='*****', skip=0, limit=10):  # noqa: E501
    """busca usuarios con ciertos parámetros

    Al pasarle ciertos parámetros devuelve usuarios que se ajusten a ellos.  # noqa: E501

    :param name: nombre del usuario
    :type name: str
    :param username: username del usuario
    :type username: str
    :param skip: number of records to skip for pagination
    :type skip: int
    :param limit: maximum number of records to return
    :type limit: int

    :rtype: List[ProfileItem]
    """

    sql = """SELECT *
            FROM (SELECT *
                    FROM get_users_by_name('{}', 100000, 0) name
                UNION
                SELECT *
                    FROM get_users_by_username('{}', 100000, 0) username
                ) found
            LIMIT {}
            OFFSET {};""".format(name, username, limit, skip)
    query = engine.execute(sql)
    found = []
    for item in query:
        profile = ProfileItem(item['id'], item['username'], item['name'])
        found.append(profile)
    return found


def search_song(name=None, author=None, genre=None, skip=None, limit=None):  # noqa: E501
    """busca canciones con ciertos parámetros

    Al pasarle ciertos parámetros devuelve cancionese que se ajusten a ellos  # noqa: E501

    :param name: nombre de la canción
    :type name: str
    :param author: autor de la canción
    :type author: str
    :param genre: genero de la canción
    :type genre: str
    :param skip: number of records to skip for pagination
    :type skip: int
    :param limit: maximum number of records to return
    :type limit: int

    :rtype: List[SongItem]
    """
    return 'do some magic!'
