##
# UploadHandler.py
# Handler for uploading images
##

from google.appengine.api import users

from google.appengine.ext.webapp import blobstore_handlers

from app.models.Photo import Photo

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    # Verifies the user is logged in
    def verifyLogin(self):
        currentUser = users.get_current_user()
        if currentUser == None:
            self.redirect(users.create_login_url(self.request.uri))
        elif currentUser.email() != 'jpoloney@gmail.com':
            self.redirect("/")
    
    def post (self):
        self.verifyLogin()
        
        if self.get_uploads('image'):
            photo = Photo()
            photo.name = self.request.get('name')
            photo.description = self.request.get('description')
            photo.albumId = int(self.request.get('albumId'))
            
            uploadFiles = self.get_uploads('image')
            blobInfo = uploadFiles[0]
            if blobInfo:
                # regenerate the thumbnail for the photo
                photo.image = blobInfo.key()
                photo.regenerateThumbnail()
        
            photo.content = self.request.get('content')
            photo.put()
            
        self.redirect('/admin')
