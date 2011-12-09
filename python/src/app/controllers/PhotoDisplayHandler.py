##
# PhotoDisplayHandler.py
# Handler for displaying images
##

import urllib

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

from app.controllers.BaseHandler import BaseHandler
from app.models.Photo import Photo

class ViewImage(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info)
        
class ViewThumb(BaseHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        photo = Photo.get(resource)
        self.response.headers['Content-Type'] = "image/jpeg"
        self.response.out.write(photo.thumbnail)
        
class ViewPhoto(BaseHandler):
    def get(self, resource):
        photoId = int(urllib.unquote(resource))
        photo = Photo.get_by_id(photoId)
        if photo:
            prevPhoto = photo.getPrevPhoto()
            nextPhoto = photo.getNextPhoto()
        
        params = {
            'photo':photo,
            'title':photo.getAlbum().name,
            'prev':prevPhoto,
            'next':nextPhoto,
            'rightCol':'rightCol/photo.html'
        }
            
        self.display('photo.html', params)
