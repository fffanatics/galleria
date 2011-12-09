##
# Category.py
# Model for categories
##

from google.appengine.ext import db

from app.models.Album import Album

class Category(db.Model):
    # Basic information about this photo
    name = db.StringProperty()
    description = db.StringProperty()
    
    # Put method for the album
    def put(self):
        db.Model.put(self)
        
    # Delete method for the album
    def delete(self):
        for album in self.getAlbums():
            album.delete()
        db.Model.delete(self)
    
    # Returns an edit link for this category
    def getEditLink(self):
        return "/admin?action=editcategory&id=" + str(self.key().id())
    
    # Returns an array of all the albums in this category, ordered by most recently added
    def getAlbums(self):
        return Album.gql("WHERE catId = :id ORDER BY created DESC", id=int(self.key().id()))
    
    def getPermLink(self):
        return "/category/" + str(self.key().id());
