'''
' SearchHandler.py
' Handler for searching for photos 
'''

import logging

from app.models.Photo import Photo

from BaseHandler import BaseHandler

class SearchHandler(BaseHandler):
    def get(self):
        term = self.request.get('s')
        
        photos = Photo.all().search(term, properties=['name', 'description']).order('name')
        logging.info(photos.count())
        params={
            'term':term,
            'photos':photos,
            'hasPhotos':photos.count() > 0
        }
        self.display('search.html', params)