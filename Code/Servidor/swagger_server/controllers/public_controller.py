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
from swagger_server.models.friend_item import FriendItem  # noqa: E501
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
    sql = "SELECT * FROM get_album_by_id( {} )".format(albumID)
    query = engine.execute(sql)
    datos = query.first()
    if datos['id'] is None:
        return 'Not found', 404

    sql2 = "SELECT * FROM get_author_name_by_id( {} )".format(datos['authorid'])
    query2 = engine.execute(sql2)
    datos2 = query2.first()

    sql3 = "SELECT * FROM get_songs_of_album( {} )".format(albumID)
    query3 = engine.execute(sql3)
    songs = []
    for item in query3:
        genero = []
        genero.append(item[4])
        song = SongItem(item[0], item[1], item[2], datos['authorid'], datos2[0],
                        albumID, datos['name'], genero)
        songs.append(song)

    return AlbumItem(datos['id'], datos['name'], datos['authorid'], datos2[0], datos['publishdate'],
                     datos['description'], songs)


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
    sql = "SELECT * FROM get_author_by_id( {} )".format(authorID)
    query = engine.execute(sql)
    datos = query.first()

    if datos['id'] is None:
        return 'Not found', 404

    sql2 = "SELECT * FROM get_album_by_authorid( {} , 10000, 0)".format(authorID)
    query2 = engine.execute(sql2)

    albums = []

    for item in query2:
        sql3 = "SELECT * FROM get_songs_of_album( {} )".format(item[0])
        query3 = engine.execute(sql3)

        songs = []

        for item2 in query3:
            genero = []
            genero.append(item2[4])
            song = SongItem(item2[0], item2[1], item2[2], authorID, datos['name'], item[0], item[1], genero)
            songs.append(song)

        album = AlbumItem(item[0], item[1], authorID, datos['name'], item[2], item[4], songs)
        albums.append(album)

    return AuthorItem(datos['id'], datos['name'], datos['bio'], albums)


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

    sql = "SELECT * FROM get_list_by_id( {} )".format(playlistID)
    query = engine.execute(sql)
    datos = query.first()
    if datos['id'] is None:
        return 'Not found', 404

    sql2 = "SELECT * FROM get_userinfo_by_id( {} )".format(datos[2])
    query2 = engine.execute(sql2)
    datos2 = query2.first()

    sql3 = "SELECT * FROM get_songs_of_list( {} )".format(playlistID)
    query3 = engine.execute(sql3)
    songs = []
    for item in query3:
        sql4 = "SELECT * FROM get_album_by_id( {} )".format(item[3])
        query4 = engine.execute(sql4)

        datos4 = query4.first()

        sql5 = "SELECT * FROM get_author_name_by_id( {} )".format(datos4[3])
        query5 = engine.execute(sql5)

        datos5 = query5.first()

        genero = []
        genero.append(item[4])

        song = SongItem(item[0], item[1], item[2], datos4[3], datos5[0], item[3], datos4[1], genero)
        songs.append(song)

    return PlaylistItem(datos[0], datos[1], datos[2], datos2[2], datos[3], datos[4], songs)


def get_profile(profileID):  # noqa: E501
    """obtiene un perfil de usuario identificado por profileID

    Obtiene un perfil de usuario identificado por profileID.  # noqa: E501

    :param profileID: ID del perfil
    :type profileID: str

    :rtype: ProfileItem
    """

    sql = "SELECT * FROM get_userinfo_by_id( {} )".format(profileID)
    query = engine.execute(sql)
    datos = query.first()
    if datos['id'] is None:
        return 'Not found', 404

    sql2 = "SELECT * FROM get_followed_by_user( {} , 10000, 0)".format(profileID)
    query2 = engine.execute(sql2)
    friends = []
    for item in query2:
        friend = FriendItem(item[0], item[1], item[2], item[3])
        friends.append(friend)

    sql3 = "SELECT * FROM get_list_by_ownerid( {} , 10000, 0)".format(profileID)
    query3 = engine.execute(sql3)
    lists = []
    for item in query3:
        sql4 = "SELECT * FROM get_songs_of_list( {} )".format(item[0])
        query4 = engine.execute(sql4)
        songs = []
        for item2 in query4:
            sql5 = "SELECT * FROM get_album_by_id( {} )".format(item2[3])
            query5 = engine.execute(sql5)

            datos5 = query5.first()

            sql6 = "SELECT * FROM get_author_name_by_id( {} )".format(datos5[3])
            query6 = engine.execute(sql6)

            datos6 = query6.first()

            genero = []
            genero.append(item2[4])
            song = SongItem(item2[0], item2[1], item2[2], datos5[3], datos6[0], item2[3], datos5[1], genero)
            songs.append(song)
        list = PlaylistItem(item[0], item[1], item[2], datos[2], item[3], item[4], songs)
        lists.append(list)
    return ProfileItem(datos[0], datos[1], datos[2], datos[3], friends, lists)

def get_song(songID):  # noqa: E501
    """obtiene información de una canción

    Obtiene los datos de la canción identificada por songID  # noqa: E501

    :param songID: ID de la canción
    :type songID: str

    :rtype: SongItem
    """

    sql = "SELECT * FROM get_songinfo_by_id( {} )".format(songID)
    query = engine.execute(sql)
    datos = query.first()
    if datos['id'] is None:
        return 'Not found', 404

    sql2 = "SELECT * FROM get_album_by_id( {} )".format(datos[3])
    query2 = engine.execute(sql2)

    datos2 = query2.first()

    sql3 = "SELECT * FROM get_author_name_by_id( {} )".format(datos2[3])
    query3 = engine.execute(sql3)

    datos3 = query3.first()
    genero = []
    genero.append(datos[4])

    return SongItem(datos[0], datos[1], datos[2], datos2[3], datos3[0], datos[3], datos2[1], genero)



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

    return AccountItem(usuario['id'], usuario['username'], usuario['name'], usuario['bio'], usuario['email'])


def search_album(name='*****', author='*****', skip=0, limit=10):  # noqa: E501
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
    sql = "SELECT * FROM search_album( '{}' , '{}' , {} , {} )".format(name, author, limit, skip)
    query = engine.execute(sql)
    albums = []
    for item in query:
        sql2 = "SELECT * FROM get_author_name_by_id( {} )".format(item[3])
        query2 = engine.execute(sql2)
        datos = query2.first()

        sql3 = "SELECT * FROM get_songs_of_album( {} )".format(item[0])
        query3 = engine.execute(sql3)
        songs = []
        for item2 in query3:
            genero = []
            genero.append(item2[4])
            song = SongItem(item2[0], item2[1], item2[2], item[3], datos[0], item[0], item[1], genero)
            songs.append(song)
        album = AlbumItem(item[0], item[1], item[3], datos[0], item[2], item[4], songs)
        albums.append(album)
    return albums


def search_authors(name='*****', skip=0, limit=10):  # noqa: E501
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
    sql = "SELECT * FROM search_author( '{}' , {} , {} )".format(name, limit, skip)
    query = engine.execute(sql)
    authors = []
    for item in query:
        sql2 = "SELECT * FROM get_album_by_authorid( {} ,10000, 0)".format(item[0])
        query2 = engine.execute(sql2)
        albums = []
        for item2 in query2:
            sql3 = "SELECT * FROM get_songs_of_album( {} )".format(item2[0])
            query3 = engine.execute(sql3)
            songs = []
            for item3 in query3:
                genero = []
                genero.append(item3[4])
                song = SongItem(item3[0], item3[1], item3[2], item[0], item[1], item2[0], item2[1], genero)
                songs.append(song)
            album = AlbumItem(item2[0], item2[1], item[0], item[1], item2[2], item2[4], songs)
            albums.append(album)
        author = AuthorItem(item[0], item[1], item[2], albums)
        authors.append(author)
    return authors


def search_playlist(name='*****', owner='*****', skip=0, limit=10):  # noqa: E501
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

    sql = "SELECT * FROM search_lists( '{}' , '{}' , {} , {} )".format(name, owner, limit, skip)
    query = engine.execute(sql)
    lists = []
    for item in query:
        sql2 = "SELECT * FROM get_userinfo_by_id( {} )".format(item[2])
        query2 = engine.execute(sql2)
        datos2 = query2.first()

        sql4 = "SELECT * FROM get_songs_of_list( {} )".format(item[0])
        query4 = engine.execute(sql4)
        songs = []
        for item3 in query4:
            sql5 = "SELECT * FROM get_album_by_id( {} )".format(item3[3])
            query5 = engine.execute(sql5)
            datos5 = query5.first()

            sql6 = "SELECT * FROM get_author_name_by_id( {} )".format(datos5[3])
            query6 = engine.execute(sql6)
            datos6 = query6.first()

            genero = []
            genero.append(item3[4])
            song = SongItem(item3[0], item3[1], item3[2], datos5[3], datos6[0], item3[3], datos5[1], genero)
            songs.append(song)

        playlist = PlaylistItem(item[0], item[1], item[2], datos2[2], item[3], item[4], songs)
        lists.append(playlist)
    return lists


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
    sql = "SELECT * FROM search_users( '{}' , '{}' , {}, {} )".format(name, username, limit, skip)
    query = engine.execute(sql)
    users = []

    for item in query:
        sql2 = "SELECT * FROM get_followed_by_user( {} , 10000, 0)".format(item[0])
        query2 = engine.execute(sql2)
        friends = []
        for item2 in query2:
            friend = FriendItem(item2[0], item2[1], item2[2], item2[3])
            friends.append(friend)

        sql3 = "SELECT * FROM get_list_by_ownerid( {} , 10000, 0)".format(item[0])
        query3 = engine.execute(sql3)
        lists = []
        for item2 in query3:
            sql4 = "SELECT * FROM get_songs_of_list( {} )".format(item2[0])
            query4 = engine.execute(sql4)
            songs = []
            for item3 in query4:
                sql5 = "SELECT * FROM get_album_by_id( {} )".format(item3[3])
                query5 = engine.execute(sql5)
                datos5 = query5.first()

                sql6 = "SELECT * FROM get_author_name_by_id( {} )".format(datos5[3])
                query6 = engine.execute(sql6)
                datos6 = query6.first()

                genero = []
                genero.append(item3[4])
                song = SongItem(item3[0], item3[1], item3[2], datos5[3], datos6[0], item3[3], datos5[1], genero)
                songs.append(song)

            list = PlaylistItem(item2[0], item2[1], item2[2], item[2], item2[3], item2[4], songs)
            lists.append(list)
        user = ProfileItem(item[0], item[1], item[2], item[3], friends, lists)
        users.append(user)

    return users


def search_song(name='*****', author='******', genre='******', skip=0, limit=10):  # noqa: E501
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
    sql = "SELECT * FROM search_songs( '{}' , '{}' , '{}' , {} , {} )".format(name, author, genre, limit, skip)
    query = engine.execute(sql)
    songs = []

    for item in query:
        sql2 = "SELECT * FROM get_album_by_id( {} )".format(item[3])
        query2 = engine.execute(sql2)

        datos2 = query2.first()

        sql3 = "SELECT * FROM get_author_name_by_id( {} )".format(datos2[3])
        query3 = engine.execute(sql3)

        datos3 = query3.first()

        genero = []
        genero.append(item[4])
        song = SongItem(item[0], item[1], item[2], datos2[3], datos3[0], item[3], datos2[1], genero)
        songs.append(song)
    return songs
