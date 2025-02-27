from fastapi.testclient import TestClient

from crate_digger.main import app
from crate_server.models.artist_query import ArtistQuery

HOST_URL   = "http://localhost:8000"
ARTIST_URL = f"{HOST_URL}/artist"

test_client = TestClient(app)
    
def test_artist_response_successful():
    query = ArtistQuery(genre="hip-hop", country="USA")
    response = test_client.post(ARTIST_URL, json=query.model_dump())
    assert response.status_code == 200
