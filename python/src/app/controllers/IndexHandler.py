'''
' IndexHandler.py
' Main Handler for the application
'''

from app.models.Category import Category

from BaseHandler import BaseHandler

class IndexHandler(BaseHandler):
    def get(self):
        categories = Category.gql("ORDER BY created DESC")
        
        params={
            'categories':categories
        }
        self.display('index.html', params)