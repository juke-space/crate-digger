import pytest

from crate_digger.main import app
from crate_server.models.artist_query import ArtistQuery
from fastapi.testclient import TestClient

HOST_URL = "http://localhost:8000"

@pytest.fixture
def test_client():
    yield TestClient(app)
    
@pytest.fixture
def artist_url():
    yield f"{HOST_URL}/artist"
    
def test_artist_query(test_client, artist_url):
    query = ArtistQuery(genre="hip-hop", country="USA")
    response = test_client.post(artist_url, json=query.model_dump())
    assert response.status_code == 200
