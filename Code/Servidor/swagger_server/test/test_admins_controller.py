# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.album_item import AlbumItem  # noqa: E501
from swagger_server.models.album_item_new import AlbumItemNew  # noqa: E501
from swagger_server.models.song_item import SongItem  # noqa: E501
from swagger_server.models.song_item_new import SongItemNew  # noqa: E501
from swagger_server.test import BaseTestCase


class TestAdminsController(BaseTestCase):
    """AdminsController integration test stubs"""

    def test_add_album(self):
        """Test case for add_album

        crea un álbum
        """
        albumItem = AlbumItemNew()
        response = self.client.open(
            '/api/albums',
            method='POST',
            data=json.dumps(albumItem),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_add_album_song(self):
        """Test case for add_album_song

        añade una canción a un album
        """
        songID = 'songID_example'
        response = self.client.open(
            '/api/albums/{albumID}/songs'.format(albumID='albumID_example'),
            method='POST',
            data=json.dumps(songID),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_add_song(self):
        """Test case for add_song

        añade una canción
        """
        songItem = SongItemNew()
        response = self.client.open(
            '/api/songs',
            method='POST',
            data=json.dumps(songItem),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_album(self):
        """Test case for delete_album

        elimina un álbum
        """
        response = self.client.open(
            '/api/albums/{albumID}'.format(albumID='albumID_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_album_image(self):
        """Test case for delete_album_image

        elimina la carátula de un álbum
        """
        response = self.client.open(
            '/api/albums/{albumID}/image'.format(albumID='albumID_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_author_image(self):
        """Test case for delete_author_image

        elimina la imagen de un autor
        """
        response = self.client.open(
            '/api/authors/{authorID}/image'.format(authorID='authorID_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_song(self):
        """Test case for delete_song

        elimina una canción
        """
        response = self.client.open(
            '/api/songs/{songID}'.format(songID='songID_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_song_file(self):
        """Test case for delete_song_file

        elimina el archivo de audio de una canción
        """
        response = self.client.open(
            '/api/songs/{songID}/file'.format(songID='songID_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_song_image(self):
        """Test case for delete_song_image

        elimina la carátula de una canción
        """
        response = self.client.open(
            '/api/songs/{songID}/image'.format(songID='songID_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_song(self):
        """Test case for update_song

        actualiza la información de una canción
        """
        songItem = SongItemNew()
        response = self.client.open(
            '/api/songs/{songID}'.format(songID='songID_example'),
            method='PUT',
            data=json.dumps(songItem),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_upload_album_image(self):
        """Test case for upload_album_image

        carga la carátula de un álbum
        """
        data = dict(albumImage=(BytesIO(b'some file data'), 'file.txt'))
        response = self.client.open(
            '/api/albums/{albumID}/image'.format(albumID='albumID_example'),
            method='POST',
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_upload_author_image(self):
        """Test case for upload_author_image

        carga la imagen e un autor
        """
        data = dict(authorImage=(BytesIO(b'some file data'), 'file.txt'))
        response = self.client.open(
            '/api/authors/{authorID}/image'.format(authorID='authorID_example'),
            method='POST',
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_upload_song_file(self):
        """Test case for upload_song_file

        carga el archivo de audio de una canción
        """
        data = dict(songFile=(BytesIO(b'some file data'), 'file.txt'))
        response = self.client.open(
            '/api/songs/{songID}/file'.format(songID='songID_example'),
            method='POST',
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_upload_song_image(self):
        """Test case for upload_song_image

        carga la carátula de una canción
        """
        data = dict(songImage=(BytesIO(b'some file data'), 'file.txt'))
        response = self.client.open(
            '/api/songs/{songID}/image'.format(songID='songID_example'),
            method='POST',
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
