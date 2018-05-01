import connexion
import six

from swagger_server.models.account_item import AccountItem  # noqa: E501
from swagger_server.models.account_item_update import AccountItemUpdate  # noqa: E501
from swagger_server.models.login_item import LoginItem  # noqa: E501
from swagger_server.models.playlist_item import PlaylistItem  # noqa: E501
from swagger_server.models.playlist_item_new import PlaylistItemNew  # noqa: E501
from swagger_server.models.session_item import SessionItem  # noqa: E501
from swagger_server import util

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
    return 'do some magic!'


@auth.enforce_auth
def add_playlist_song(playlistID, songID=None):  # noqa: E501
    """añade una canción a una lista de reproducción

    Un usuario añade una canción a una lista de reproducción de su propiedad. # noqa: E501

    :param playlistID: ID de la playlist
    :type playlistID: str
    :param songID: Song to add
    :type songID: str

    :rtype: PlaylistItem
    """
    return 'do some magic!'


@auth.enforce_auth
def delete_account():  # noqa: E501
    """borra la cuenta del usuario

    Elimina definitivamente la cuenta del usuario. No se puede deshacer. No funciona con cuentas de administrador  # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


@auth.enforce_auth
def delete_playlist(playlistID):  # noqa: E501
    """elimina una playlist

    Elimina la playlist identificada por playlistID  # noqa: E501

    :param playlistID: ID de la playlist
    :type playlistID: str

    :rtype: None
    """
    return 'do some magic!'


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
    return 'do some magic!'


@auth.enforce_auth
def follow_profile(profileID):  # noqa: E501
    """comienza a seguir al usuario identificado por profileID

    Comienza a seguir al usuario identificado por profileID # noqa: E501

    :param profileID: ID del perfil
    :type profileID: str

    :rtype: None
    """
    return 'do some magic!'


@auth.enforce_auth
def get_account():  # noqa: E501
    """devuelve la información de la cuenta del usuario

    Devuelve la información de la cuenta del usuario.  # noqa: E501


    :rtype: AccountItem
    """
    return 'do some magic!'


@auth.enforce_auth
def logout():  # noqa: E501
    """cierra sesión de usuario

    Cierra la sesión de usuario # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


@auth.enforce_auth
def restore_session():  # noqa: E501
    """devuelve información de sincronización de canciones

    Devuelve la lista de reproducción, la canción y el segundo que estaba escuchando el usuario previamente  # noqa: E501


    :rtype: SessionItem
    """
    return 'do some magic!'


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
    return 'do some magic!'


@auth.enforce_auth
def unfollow_profile(profileID):  # noqa: E501
    """deja de seguir al usuario identificado por profileID

    Deja de seguir al usuario identificado por profileID  # noqa: E501

    :param profileID: ID del perfil
    :type profileID: str

    :rtype: None
    """
    return 'do some magic!'


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
    return 'do some magic!'


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
    return 'do some magic!'


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
    if connexion.request.is_json:
        playlistItem = PlaylistItemNew.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
