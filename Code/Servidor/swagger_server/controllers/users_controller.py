import connexion
import six

from swagger_server.models.account_item import AccountItem  # noqa: E501
from swagger_server.models.account_item_update import AccountItemUpdate  # noqa: E501
from swagger_server.models.login_item import LoginItem  # noqa: E501
from swagger_server.models.playlist_item import PlaylistItem  # noqa: E501
from swagger_server.models.playlist_item_new import PlaylistItemNew  # noqa: E501
from swagger_server.models.session_item import SessionItem  # noqa: E501
from swagger_server.models.friend_item import FriendItem  #noga: E501
from swagger_server.models.song_item import SongItem  #noga: E501
from swagger_server import util

from swagger_server.database import engine
import swagger_server.authentificator as auth


@auth.enforce_auth
def add_playlist(playlistItem=None):  # noqa: E501
    """crea una lista de reproducción

    Un usuario crea una lista de reproducción. # noqa: E501

    :param playlistItem: Playlist item to add
    :type playlistItem: dict | bytes

    :rtype: PlaylistItem
    """
    if connexion.request.is_json:
        playlistItem = PlaylistItemNew.from_dict(connexion.request.get_json())  # noqa: E501

    sql = "SELECT * FROM insert_new_play_list( '{}' , {} , '{}' ); COMMIT;"\
        .format(playlistItem.name, auth.get_userid(), playlistItem.description)
    engine.execute(sql)

    sql = "SELECT * FROM search_one_list( {} , '{}' , '{}' )".\
        format(auth.get_userid(), playlistItem.description, playlistItem.name)
    query = engine.execute(sql)
    newdatos = query.first()

    sql = "SELECT * FROM get_list_by_id( {} )".format(newdatos[0])
    query = engine.execute(sql)
    datos = query.first()
    if datos['id'] is None:
        return 'Not found', 404

    sql2 = "SELECT * FROM get_userinfo_by_id( {} )".format(datos[2])
    query2 = engine.execute(sql2)
    datos2 = query2.first()

    sql3 = "SELECT * FROM get_songs_of_list( {} )".format(newdatos[0])
    query3 = engine.execute(sql3)
    songs = []
    for item in query3:
        sql4 = "SELECT * FROM get_album_by_id( {} )".format(item[3])
        query4 = engine.execute(sql4)

        datos4 = query4.first()

        sql5 = "SELECT * FROM get_author_name_by_id( {} )".format(datos4[3])
        query5 = engine.execute(sql5)

        datos5 = query5.first()
        song = SongItem(item[0], item[1], item[2], datos4[3], datos5[0], item[3], datos4[1], item[4])
        songs.append(song)

    return PlaylistItem(datos[0], datos[1], datos[2], datos2[2], datos[3], datos[4], songs)


@auth.enforce_auth
def add_playlist_song(playlistID, songID = None):  # noqa: E501
    """añade una canción a una lista de reproducción

    Un usuario añade una canción a una lista de reproducción de su propiedad. # noqa: E501

    :param playlistID: ID de la playlist
    :type playlistID: str
    :param songID: Song to add
    :type songID: str

    :rtype: PlaylistItem
    """
    sql = "SELECT * FROM check_list_user( {} , {} )".format(auth.get_userid(), playlistID)
    query = engine.execute(sql)
    datos = query.first()

    if datos[0] == 0:
        return 'Not found', 404

    sql = "SELECT * FROM get_songinfo_by_id( {} )".format(int(songID))
    query = engine.execute(sql)
    datos = query.first()
    if datos['id'] is None:
        return 'Not found', 404

    sql = "SELECT * FROM insert_song_in_list( {} , {} ); COMMIT;".format(playlistID, int(songID))
    engine.execute(sql)

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
        song = SongItem(item[0], item[1], item[2], datos4[3], datos5[0], item[3], datos4[1], item[4])
        songs.append(song)

    return PlaylistItem(datos[0], datos[1], datos[2], datos2[2], datos[3], datos[4], songs)


@auth.enforce_auth
def delete_account():  # noqa: E501
    """borra la cuenta del usuario

    Elimina definitivamente la cuenta del usuario. No se puede deshacer. No funciona con cuentas de administrador  # noqa: E501


    :rtype: None
    """
    sql = "SELECT * FROM del_user( {} ); COMMIT;".format(auth.get_userid())
    engine.execute(sql)

    auth.sign_out()


@auth.enforce_auth
def delete_playlist(playlistID):  # noqa: E501
    """elimina una playlist

    Elimina la playlist identificada por playlistID  # noqa: E501

    :param playlistID: ID de la playlist
    :type playlistID: str

    :rtype: None
    """
    sql = "SELECT * FROM check_list_user( {} , {} )".format(auth.get_userid(), playlistID)
    query = engine.execute(sql)
    datos = query.first()

    if datos[0] == 0:
        return 'Not found', 404

    sql = "SELECT * FROM del_list( {}); COMMIT;".format(playlistID)
    engine.execute(sql)


@auth.enforce_auth
def delete_playlist_song(playlistID, songID):  # noqa: E501
    """elimina una canción de una playlist identificada por playlistID

    Elimina una canción de la playlist identificada por playlistID  # noqa: E501

    :param playlistID: ID de la playlist
    :type playlistID: str
    :param songID: ID de la canción
    :type songID: str

    :rtype: None
    """
    sql = "SELECT * FROM check_list_user( {} , {} )".format(auth.get_userid(), playlistID)
    query = engine.execute(sql)
    datos = query.first()

    if datos[0] == 0:
        return 'Not found', 404

    sql = "SELECT * FROM del_list_song ( {} , {} ); COMMIT;".format(playlistID, songID)
    engine.execute(sql)


@auth.enforce_auth
def follow_profile(profileID):  # noqa: E501
    """comienza a seguir al usuario identificado por profileID

    Comienza a seguir al usuario identificado por profileID # noqa: E501

    :param profileID: ID del perfil
    :type profileID: str

    :rtype: None
    """

    sql = "SELECT * FROM get_userinfo_by_id( {} )".format(profileID)
    query = engine.execute(sql)
    datos = query.first()
    if datos['id'] is None:
        return 'Not found', 404
    sql = "SELECT * FROM follow_user( {} , {} ); COMMIT;".format(auth.get_userid(), profileID)
    engine.execute(sql)



@auth.enforce_auth
def get_account():  # noqa: E501
    """devuelve la información de la cuenta del usuario

    Devuelve la información de la cuenta del usuario.  # noqa: E501


    :rtype: AccountItem
    """
    sql = "SELECT * FROM get_user_by_id( {} )".format(auth.get_userid())
    query = engine.execute(sql)
    datos = query.first()
    if datos['id'] is None:
        return 'Not found', 404

    sql2 = "SELECT * FROM get_followed_by_user( {} , 10000, 0)".format(auth.get_userid())
    query2 = engine.execute(sql2)
    friends = []
    for item in query2:
        friend = FriendItem(item[0], item[1], item[2], item[3])
        friends.append(friend)

    sql3 = "SELECT * FROM get_list_by_ownerid( {} , 10000, 0)".format(auth.get_userid())
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
            song = SongItem(item2[0], item2[1], item2[2], datos5[3], datos6[0], item2[3], datos5[1], item2[4])
            songs.append(song)
        list = PlaylistItem(item[0], item[1], item[2], datos[3], item[3], item[4], songs)
        lists.append(list)
    return AccountItem(datos[0], datos[1], datos[3], datos[4], datos[2], friends, lists)


@auth.enforce_auth
def logout():  # noqa: E501
    """cierra sesión de usuario

    Cierra la sesión de usuario # noqa: E501


    :rtype: None
    """
    auth.sign_out()


@auth.enforce_auth
def restore_session():  # noqa: E501
    """devuelve información de sincronización de canciones

    Devuelve la lista de reproducción, la canción y el segundo que estaba escuchando el usuario previamente  # noqa: E501


    :rtype: SessionItem
    """
    sql = " SELECT * FROM get_session( {} )".format(auth.get_userid())
    query = engine.execute(sql)
    datos = query.first()

    return SessionItem(datos[2], datos[3], datos[4])


@auth.enforce_auth
def save_session(sessionItem=None):  # noqa: E501
    """guarda información de sincronización de canciones

    Guarda la lista de reproducción, la canción y el segundo que está escuchando el usuario # noqa: E501

    :param sessionItem: Datos a sincronizar
    :type sessionItem: dict | bytes

    :rtype: AccountItem
    """
    if connexion.request.is_json:
        sessionItem = SessionItem.from_dict(connexion.request.get_json())  # noqa: E501

    sql = "SELECT * FROM update_user_session( {} , {} , {} , {} ); COMMIT;"\
        .format(auth.get_userid(), int(sessionItem.playlist_id), int(sessionItem.song_id), int(sessionItem.second))
    engine.execute(sql)
    return get_account()


@auth.enforce_auth
def unfollow_profile(profileID):  # noqa: E501
    """deja de seguir al usuario identificado por profileID

    Deja de seguir al usuario identificado por profileID  # noqa: E501

    :param profileID: ID del perfil
    :type profileID: str

    :rtype: None
    """
    sql = "SELECT * FROM get_userinfo_by_id( {} )".format(profileID)
    query = engine.execute(sql)
    datos = query.first()
    if datos['id'] is None:
        return 'Not found', 404
    sql = "SELECT * FROM unfollow_user( {} , {} ); COMMIT;".format(auth.get_userid(), profileID)
    engine.execute(sql)


@auth.enforce_auth
def update_account(accountItem=None):  # noqa: E501
    """actualiza información de cuenta de usuario

    Actualiza la información de la cuenta del usuario. El campo \&quot;friends\&quot; de los amigos de un usuario está siempre vacío (valor NULL) # noqa: E501

    :param accountItem: Datos a actualizar
    :type accountItem: dict | bytes

    :rtype: AccountItem
    """
    if connexion.request.is_json:
        accountItem = AccountItemUpdate.from_dict(connexion.request.get_json())  # noqa: E501

    sql = "SELECT * FROM update_user( {} , '{}' , '{}' , '{}' ); COMMIT;"\
        .format(auth.get_userid(), accountItem.bio, accountItem.name, accountItem.username)
    engine.execute(sql)
    return get_account()


@auth.enforce_auth
def update_account_credentials(loginItem=None):  # noqa: E501
    """modifica credenciales de acceso de cuenta de usuario

    Modifica las credenciales de acceso de la cuenta del usuario. El campo \&quot;friends\&quot; de los amigos de un usuario está siempre vacío (valor NULL) # noqa: E501

    :param loginItem: Datos a actualizar
    :type loginItem: dict | bytes

    :rtype: AccountItem
    """
    if connexion.request.is_json:
        loginItem = LoginItem.from_dict(connexion.request.get_json())  # noqa: E501
    sql = "SELECT * FROM update_user_credentials( {} , '{}' , '{}' ); COMMIT;"\
        .format(auth.get_userid(), loginItem.mail, loginItem._pass)
    engine.execute(sql)
    return get_account()


@auth.enforce_auth
def update_playlist(playlistID, playlistItem=None):  # noqa: E501
    """actualiza la información de una playlist

    Un usuario actualiza la información de una playlist de su propiedad. # noqa: E501

    :param playlistID: ID de la playlist
    :type playlistID: str
    :param playlistItem: Playlist item to update
    :type playlistItem: dict | bytes

    :rtype: PlaylistItem
    """
    sql = "SELECT * FROM check_list_user( {} , {} )".format(auth.get_userid(), playlistID)
    query = engine.execute(sql)
    datos = query.first()

    if datos[0] == 0:
        return 'Not found', 404

    if connexion.request.is_json:
        playlistItem = PlaylistItemNew.from_dict(connexion.request.get_json())  # noqa: E501

    sql = "SELECT * FROM update_list( {} , '{}' , '{}' ); COMMIT;"\
        .format(playlistID, playlistItem.name, playlistItem.description)
    engine.execute(sql)

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
        song = SongItem(item[0], item[1], item[2], datos4[3], datos5[0], item[3], datos4[1], item[4])
        songs.append(song)

    return PlaylistItem(datos[0], datos[1], datos[2], datos2[2], datos[3], datos[4], songs)
