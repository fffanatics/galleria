##
# Album.py
# Model for albums
##

import re

from google.appengine.ext import db

from app.models.Photo import Photo

class Album(db.Model):
    # Basic information about this photo
    name = db.StringProperty()
    description = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty()
    thumbnailId = db.IntegerProperty()
    catId = db.IntegerProperty()
    
    # Put method for the album
    def put(self):
        db.Model.put(self)
        
    # Delete method for the album
    def delete(self):
        for photo in self.getPhotos():
            photo.delete()
        db.Model.delete(self)
    
    # Returns an edit link for this album
    def getEditLink(self):
        return "/admin?action=editalbum&id=" + str(self.key().id())
    
    # Returns an array of all the photos in this album, ordered by most recently added
    def getPhotos(self):
        return Photo.gql("WHERE albumId = :id ORDER BY created DESC", id=int(self.key().id()))
    
    def getPermLink(self):
        cleanName = re.sub('(\s)*(\W)*', '', self.name)
        return "/album/" + str(self.key().id()) + "/" + cleanName;
    
    # Returns the image that is the thumbnail image for this album
    def getThumbnail(self):
        photo = None
        if self.thumbnailId:
            photo = Photo.get_by_id(self.thumbnailId)
        else:
            photos = self.getPhotos()
            for photo in photos:
                break;
            
        return photo;

    # Returns the category that this album belongs to
    def getCategory(self):
        from app.models.Category import Category
        return Category.get_by_id(self.catId)