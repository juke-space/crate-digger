if not __name__ == '__main__':
    exit()

import uvicorn
from fastapi import FastAPI

from crate_server.apis.default_api_base import BaseDefaultApi
from crate_server.apis.default_api      import router
from crate_server.models.artist         import Artist
from crate_server.models.artist_query   import ArtistQuery

app = FastAPI()
app.include_router(router)

# TODO: Move to separate module (out of main)
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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
