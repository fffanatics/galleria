##
# CategoryDisplayHandler.py
# Handler for displaying the albums in a category
##

import urllib

from app.models.Category import Category

from BaseHandler import BaseHandler

class ViewCategory(BaseHandler):
    def get(self, resource):
        catId = int(urllib.unquote(resource))
        category = Category.get_by_id(catId)
        
        params={
            'category':category,
            'title':category.name
        }
        self.display('category.html', params)