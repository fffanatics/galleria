from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from app.controllers.IndexHandler import IndexHandler
from app.controllers.AdminHandler import AdminHandler
from app.controllers.UploadHandler import UploadHandler
from app.controllers.SearchHandler import SearchHandler
from app.controllers.PhotoDisplayHandler import ViewImage
from app.controllers.PhotoDisplayHandler import ViewThumb
from app.controllers.PhotoDisplayHandler import ViewPhoto
from app.controllers.AlbumDisplayHandler import ViewAlbum
from app.controllers.CategoryDisplayHandler import ViewCategory

application = webapp.WSGIApplication([
                                      ('/', IndexHandler),
                                      ('/admin', AdminHandler),
                                      ('/upload', UploadHandler),
                                      ('/thumb/([^/]+)?', ViewThumb),
                                      ('/img/([^/]+)?', ViewImage),
                                      ('/album/([0-9]+)/([^/]+)', ViewAlbum),
                                      ('/photo/([0-9]+)', ViewPhoto),
                                      ('/category/([0-9]+)', ViewCategory),
                                      ('/search', SearchHandler)
                                     ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
