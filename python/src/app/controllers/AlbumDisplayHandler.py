##
# AlbumDisplayHandler.py
# Handler for displaying the contents of an album
##

import urllib

from app.models.Album import Album

from BaseHandler import BaseHandler

class ViewAlbum(BaseHandler):
    def get(self, resourceId, resourceName):
        albumId = int(urllib.unquote(resourceId))
        album = Album.get_by_id(albumId)
        
        params={
            'album':album,
            'title':album.name
        }
        self.display('album.html', params)