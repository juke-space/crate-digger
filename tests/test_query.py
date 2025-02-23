from fastapi.testclient import TestClient
from crate_digger.main import app
from crate_server.models.artist_query import ArtistQuery

test_client = TestClient(app)
BASE_URL = "http://localhost:8000"

def test_artist_query():
    query = ArtistQuery(genre="hip-hop", country="USA")
    response = test_client.post("/".join([BASE_URL, "artist"]), json=query.model_dump())
    assert response.status_code == 200
