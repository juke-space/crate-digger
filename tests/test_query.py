from fastapi.testclient import TestClient
import pytest

from crate_digger.main import app
from crate_server.models.artist_query import ArtistQuery

HOST_URL   = "http://localhost:8000"
ARTIST_URL = f"{HOST_URL}/artist"

@pytest.fixture
def test_client():
    yield TestClient(app)
    
def test_artist_response_successful(test_client):
    query = ArtistQuery(genre="hip-hop", country="USA")
    response = test_client.post(ARTIST_URL, json=query.model_dump())
    assert response.status_code == 200
