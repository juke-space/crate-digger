if not __name__ == '__main__':
    exit()

from crate_server.apis.default_api_base import BaseDefaultApi
from crate_server.models.artist         import Artist
from crate_server.models.artist_query   import ArtistQuery

class QueryApi(BaseDefaultApi):
    def search_artist(self, artist_query : ArtistQuery):
        # TODO: Remove test artist
        test_artist = Artist(
            "Test artist",
            "Test disambiguation",
            "Test genre",
            "Test life start",
            "Test life end",
            "Test country",
            "Test state_province",
            "Test municipality"
        )

        return [test_artist] 
