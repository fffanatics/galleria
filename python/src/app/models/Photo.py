##
# Photo.py
# Model for individual Photos
##

from google.appengine.api import images

from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.ext import search

class Photo(search.SearchableModel):
    # Basic information about this photo
    name = db.StringProperty()
    description = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    # The album that this photo belongs to
    albumId = db.IntegerProperty()
    # The image data associated with this photo
    image = blobstore.BlobReferenceProperty()
    thumbnail = db.BlobProperty()
    
    @classmethod
    def SearchableProperties(cls):
        return [['name', 'description']]
    
    # Put method for the photo
    def put(self):
        db.Model.put(self)
        
    # Delete method for the photo
    def delete(self):
        self.image.delete()
        db.Model.delete(self)
    
    # Returns an edit link for this photo
    def getEditLink(self):
        return "/admin?action=editphoto&id=" + str(self.key().id())
    
    # Returns a permanent link to view this photo
    def getPermLink(self):
        return "/photo/" + str(self.key().id())
    
    # Returns a link that shows the thumbnail image of this photo
    def getThumbLink(self):
        return "/thumb/" + str(self.key())
    
    # Returns a link that shows the full image of this photo
    def getImageLink(self):
        return "/img/" + str(self.image.key())
    
    # Regenerates the thumbnail for this photo
    def regenerateThumbnail(self):
        image = images.Image(blob_key=str(self.image.key()))
        image.resize(width=240)
        thumbnail = image.execute_transforms(output_encoding=images.JPEG)
        self.thumbnail = db.Blob(thumbnail)

    # Returns the album that this photo belongs to
    def getAlbum(self):
        from app.models.Album import Album
        return Album.get_by_id(self.albumId)
    
    # Returns the previous photo in this album (if it exists)
    def getPrevPhoto(self):
        album = self.getAlbum()
        allPhotos = album.getPhotos()
        prevPhoto = None
        for photo in allPhotos:
            if photo.key().id() == self.key().id():
                return prevPhoto
            prevPhoto = photo
    
    # Returns the next photo in this album (if it exists)
    def getNextPhoto(self):
        album = self.getAlbum()
        allPhotos = album.getPhotos()
        foundPhoto = False
        for photo in allPhotos:
            if foundPhoto:
                return photo
            elif photo.key().id() == self.key().id():
                foundPhoto = True
