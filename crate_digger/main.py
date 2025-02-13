if not __name__ == '__main__':
    exit()

from crate_server.apis.default_api_base import BaseDefaultApi
from crate_server.models.artist_query   import ArtistQuery

class QueryApi(BaseDefaultApi):
    def search_artist(self, artist_query : ArtistQuery):
        return [] # TODO: Do something
