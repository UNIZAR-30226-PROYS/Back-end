# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.account_item import AccountItem  # noqa: E501
from swagger_server.models.account_item_update import AccountItemUpdate  # noqa: E501
from swagger_server.models.login_item import LoginItem  # noqa: E501
from swagger_server.models.playlist_item import PlaylistItem  # noqa: E501
from swagger_server.models.playlist_item_new import PlaylistItemNew  # noqa: E501
from swagger_server.models.session_item import SessionItem  # noqa: E501
from swagger_server.test import BaseTestCase


class TestUsersController(BaseTestCase):
    """UsersController integration test stubs"""

    def test_add_playlist(self):
        """Test case for add_playlist

        crea una lista de reproducción
        """
        playlistItem = PlaylistItemNew()
        response = self.client.open(
            '/api/playlists',
            method='POST',
            data=json.dumps(playlistItem),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_add_playlist_song(self):
        """Test case for add_playlist_song

        añade una canción a una lista de reproducción
        """
        songID = 'songID_example'
        response = self.client.open(
            '/api/playlists{playlistID}/songs'.format(playlistID='playlistID_example'),
            method='POST',
            data=json.dumps(songID),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_account(self):
        """Test case for delete_account

        borra la cuenta del usuario
        """
        response = self.client.open(
            '/api/account',
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_playlist(self):
        """Test case for delete_playlist

        elimina una playlist
        """
        response = self.client.open(
            '/api/playlists/{playlistID}'.format(playlistID='playlistID_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_playlist_song(self):
        """Test case for delete_playlist_song

        elimina una canción de una playlist identificada por playlistID
        """
        response = self.client.open(
            '/api/playlists/{playlistID}/songs/{songID}'.format(playlistID='playlistID_example', songID='songID_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_follow_profile(self):
        """Test case for follow_profile

        comienza a seguir al usuario identificado por profileID
        """
        response = self.client.open(
            '/api/profiles/{profileID}/follow'.format(profileID='profileID_example'),
            method='POST',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_account(self):
        """Test case for get_account

        devuelve la información de la cuenta del usuario
        """
        response = self.client.open(
            '/api/account',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_logout(self):
        """Test case for logout

        cierra sesión de usuario
        """
        response = self.client.open(
            '/api/login',
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_restore_session(self):
        """Test case for restore_session

        devuelve información de sincronización de canciones
        """
        response = self.client.open(
            '/api/account/session',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_save_session(self):
        """Test case for save_session

        guarda información de sincronización de canciones
        """
        sessionItem = SessionItem()
        response = self.client.open(
            '/api/account/session',
            method='PUT',
            data=json.dumps(sessionItem),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_unfollow_profile(self):
        """Test case for unfollow_profile

        deja de seguir al usuario identificado por profileID
        """
        response = self.client.open(
            '/api/profiles/{profileID}/follow'.format(profileID='profileID_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_account(self):
        """Test case for update_account

        actualiza información de cuenta de usuario
        """
        accountItem = AccountItemUpdate()
        response = self.client.open(
            '/api/account',
            method='PUT',
            data=json.dumps(accountItem),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_account_credentials(self):
        """Test case for update_account_credentials

        modifica credenciales de acceso de cuenta de usuario
        """
        loginItem = LoginItem()
        response = self.client.open(
            '/api/account/credentials',
            method='PUT',
            data=json.dumps(loginItem),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_playlist(self):
        """Test case for update_playlist

        actualiza la información de una playlist
        """
        playlistItem = PlaylistItemNew()
        response = self.client.open(
            '/api/playlists/{playlistID}'.format(playlistID='playlistID_example'),
            method='PUT',
            data=json.dumps(playlistItem),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
