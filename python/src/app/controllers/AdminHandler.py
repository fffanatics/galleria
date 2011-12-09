##
# AdminHandler.py
# Handler for admin page
##

import datetime

from google.appengine.api import users
from google.appengine.ext import blobstore

from BaseHandler import BaseHandler

from app.models.Album import Album
from app.models.Photo import Photo
from app.models.Category import Category

class AdminHandler(BaseHandler):
    # Verifies the user is logged in
    def verifyLogin(self):
        currentUser = users.get_current_user()
        if currentUser == None:
            self.redirect(users.create_login_url(self.request.uri))
        elif currentUser.email() != 'jpoloney@gmail.com':
            self.redirect("/")    
            
    def get(self):
        self.handleAction()
        
    def post (self):
        self.handleAction()
            
    def handleAction(self):
        self.verifyLogin()
        
        action = self.request.get('action')
        
        params = {
            'action':action
        }
        
        if action == 'addphoto':
            albums = Album.gql("ORDER BY created DESC")
            
            if albums.count() > 0:
                params['uploadUrl'] = blobstore.create_upload_url('/upload')
            
            params['albums'] = albums
        elif action == 'addalbum':
            params['categories'] = Category.all()
            
            if self.request.get('submit'):
                album = Album()
                album.name = self.request.get('name')
                album.description = self.request.get('description')
                album.catId = int(self.request.get('catId'))
                album.modified = datetime.datetime.now()
                album.put()
                
                self.setStatus('Added new album')
                params['action'] = False
        elif action == 'editphoto':
            photoId = int(self.request.get('id'))
            photo = Photo.get_by_id(photoId)
            
            params['photo'] = photo
            params['albums'] = Album.gql("ORDER BY created DESC")
            if self.request.get('submit'):
                photo.name = self.request.get('name')
                photo.description = self.request.get('description')
                photo.albumId = int(self.request.get('albumId'))
                photo.regenerateThumbnail()
                photo.put()
                
                self.redirect(photo.getPermLink())
        elif action == 'delphoto':
            photoId = int(self.request.get('id'))
            photo = Photo.get_by_id(photoId)
            photo.delete()
            
            self.setStatus('Photo has been deleted')
            params['action'] = False
        elif action == 'editalbum':
            albumId = int(self.request.get('id'))
            album = Album.get_by_id(albumId)
            
            params['album'] = album
            params['categories'] = Category.all()
            if self.request.get('submit'):
                album.name = self.request.get('name')
                album.description = self.request.get('description')
                album.catId = int(self.request.get('catId'))
                album.modified = datetime.datetime.now()
                album.put()
                
                self.redirect(album.getPermLink())
        elif action == 'delalbum':
            albumId = int(self.request.get('id'))
            album = Album.get_by_id(albumId)
            album.delete()
            
            self.setStatus('Album has been deleted')
            params['action'] = False
        elif action == 'addcategory':
            if self.request.get('submit'):
                category = Category()
                category.name = self.request.get('name')
                category.description = self.request.get('description')
                category.put()
                
                self.setStatus('Added new category')
                params['action'] = False
        elif action == 'editcategory':
            catId = int(self.request.get('id'))
            category = Category.get_by_id(catId)
            
            params['category'] = category
            if self.request.get('submit'):
                category.name = self.request.get('name')
                category.description = self.request.get('description')
                category.put()
                
                self.redirect(category.getPermLink())
        elif action == 'delcategory':
            catId = int(self.request.get('id'))
            category = Category.get_by_id(catId)
            category.delete()
            
            self.setStatus('Category has been deleted')
            params['action'] = False
        
        self.display('admin.html', params)
        
