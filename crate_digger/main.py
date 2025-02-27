"""
    Server entry point
"""
import uvicorn
from fastapi import FastAPI

from crate_server.apis.default_api import router
from crate_server.apis.default_api_base import BaseDefaultApi
from crate_server.models.artist import Artist
from crate_server.models.artist_query import ArtistQuery

app = FastAPI()
app.include_router(router)

class API(BaseDefaultApi):
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

if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
