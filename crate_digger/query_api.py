"""
    API methods
"""
from crate_server.apis.default_api_base import BaseDefaultApi
from crate_server.models.artist import Artist
from crate_server.models.artist_query import ArtistQuery

class QueryApi(BaseDefaultApi):
    def search_artist(self, artist_query : ArtistQuery):
        # TODO: Remove test artist
        test_artist = Artist(
            name="Test artist",
            disambiguation="Test disambiguation",
            genre="Test genre",
            life_start="Test life start",
            life_end="Test life end",
            country="Test country",
            state_province="Test state_province",
            municipality="Test municipality"
        )

        return [test_artist]
