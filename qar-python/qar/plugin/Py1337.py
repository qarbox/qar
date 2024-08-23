
from qar import Plugin
from py1337x import py1337x

class QarPy1337(Plugin):
    def __init__(self, qar):
        super().__init__(qar, "qar-py1337")
        self.torrents = py1337x(proxy='1337x.to', cache='py1337xCache', cacheTime=500)
    
    def search_movie(self, query):
        result = self.torrents.search(query, category='movies', sortBy='seeders', order='desc')
        movies = []

        for item in result.items:
            pass
    
    def search_tv(self, query):
        pass

