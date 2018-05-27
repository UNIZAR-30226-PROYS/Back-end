# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.account_item import AccountItem  # noqa: E501
from swagger_server.models.album_item import AlbumItem  # noqa: E501
from swagger_server.models.author_item import AuthorItem  # noqa: E501
from swagger_server.models.login_item import LoginItem  # noqa: E501
from swagger_server.models.playlist_item import PlaylistItem  # noqa: E501
from swagger_server.models.profile_item import ProfileItem  # noqa: E501
from swagger_server.models.sign_up_item import SignUpItem  # noqa: E501
from swagger_server.models.song_item import SongItem  # noqa: E501
from swagger_server.test import BaseTestCase


class TestPublicController(BaseTestCase):
    """PublicController integration test stubs"""

    def test_create_account(self):
        """Test case for create_account

        crea cuenta de usuario
        """
        signupItem = SignUpItem()
        response = self.client.open(
            '/api/signup',
            method='POST',
            data=json.dumps(signupItem),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_album(self):
        """Test case for get_album

        obtiene un álbum
        """
        response = self.client.open(
            '/api/albums/{albumID}'.format(albumID='albumID_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_album_image(self):
        """Test case for get_album_image

        obtiene la carátula de un álbum
        """
        response = self.client.open(
            '/api/albums/{albumID}/image'.format(albumID='albumID_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_author(self):
        """Test case for get_author

        obtiene un perfil de autor identificado por authorID
        """
        response = self.client.open(
            '/api/authors/{authorID}'.format(authorID='authorID_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_author_image(self):
        """Test case for get_author_image

        obtiene la imagen de un autor
        """
        response = self.client.open(
            '/api/authors/{authorID}/image'.format(authorID='authorID_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_playlist(self):
        """Test case for get_playlist

        obtiene una playlist
        """
        response = self.client.open(
            '/api/playlists/{playlistID}'.format(playlistID='playlistID_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_profile(self):
        """Test case for get_profile

        obtiene un perfil de usuario identificado por profileID
        """
        response = self.client.open(
            '/api/profiles/{profileID}'.format(profileID='profileID_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_song(self):
        """Test case for get_song

        obtiene información de una canción
        """
        response = self.client.open(
            '/api/songs/{songID}'.format(songID='songID_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_song_file(self):
        """Test case for get_song_file

        obtiene el archivo de audio de una canción
        """
        response = self.client.open(
            '/api/songs/{songID}/file'.format(songID='songID_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_song_image(self):
        """Test case for get_song_image

        obtiene la carátula de una canción
        """
        response = self.client.open(
            '/api/songs/{songID}/image'.format(songID='songID_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_login(self):
        """Test case for login

        inicia sesión de usuario
        """
        loginItem = LoginItem()
        response = self.client.open(
            '/api/login',
            method='POST',
            data=json.dumps(loginItem),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_search_album(self):
        """Test case for search_album

        busca álbunes con ciertos parámetros
        """
        query_string = [('name', 'name_example'),
                        ('author', 'author_example'),
                        ('skip', 1),
                        ('limit', 50)]
        response = self.client.open(
            '/api/albums',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_search_authors(self):
        """Test case for search_authors

        busca autores con ciertos parámetros
        """
        query_string = [('name', 'name_example'),
                        ('skip', 1),
                        ('limit', 50)]
        response = self.client.open(
            '/api/authors',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_search_playlist(self):
        """Test case for search_playlist

        busca listas de reproducción con ciertos parámetros
        """
        query_string = [('name', 'name_example'),
                        ('owner', 'owner_example'),
                        ('skip', 1),
                        ('limit', 50)]
        response = self.client.open(
            '/api/playlists',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_search_profiles(self):
        """Test case for search_profiles

        busca usuarios con ciertos parámetros
        """
        query_string = [('name', 'name_example'),
                        ('username', 'username_example'),
                        ('skip', 1),
                        ('limit', 50)]
        response = self.client.open(
            '/api/profiles',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_search_song(self):
        """Test case for search_song

        busca canciones con ciertos parámetros
        """
        query_string = [('name', 'name_example'),
                        ('author', 'author_example'),
                        ('genre', 'genre_example'),
                        ('skip', 1),
                        ('limit', 50)]
        response = self.client.open(
            '/api/songs',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
