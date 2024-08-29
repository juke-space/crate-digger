import uvicorn
from fastapi import FastAPI
from crate_server.apis.default_api import router
from crate_server.models.artist import Artist

app = FastAPI()

async def search_artist(artist_query:Artist):
    return "hello world!"

route_logic = {"search_artist": search_artist}

for route in router.routes:
    route.endpoint = route_logic[route.name]

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
