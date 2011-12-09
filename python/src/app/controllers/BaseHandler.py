##
# BaseHandler.py
# Base class for all controllers
##

import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from app.models.Album import Album
from app.models.Photo import Photo
from app.models.Category import Category

class BaseHandler(webapp.RequestHandler):
    # Status to display at the top of the page
    status=""
    
    # Sets the status for the post
    def setStatus(self, newStatus):
        self.status=newStatus
        
    # Displays a template
    def display(self,templateFile,params={}):
        path=os.path.join(os.path.dirname(__file__) + '/../templates/', templateFile)
        
        user=users.get_current_user()
        if user:
            isAdmin=user.email() == "jpoloney@gmail.com"
        else:
            isAdmin=False
        
        # Add some default parameters    
        params['status']=self.status
        params['APP_URL']='http://joel.poloney.com/galleria'
        params['user']=user
        params['isAdmin']=isAdmin
        
        # Get 5 most recent albums
        params['recentAlbums']=Album.gql("ORDER BY created DESC LIMIT 5")
        
        # Get All categories
        params['categories']=Category.all()
        
        # Get information for stats section
        params['numAlbums']=Album.all().count()
        params['numPhotos']=Photo.all().count()
        
        self.response.out.write(template.render(path, params))