from crate_digger.app import app
from crate_server.models.artist import Artist
from fastapi.testclient import TestClient

class TestAPI:
    @classmethod
    def setup_class(cls):
        cls.client = TestClient(app)
    
    def test_artist(self):
        test_artist = Artist(name="Saba", location="Chicago", genre="hip hop")
        reponse = self.client.post("/artists", json=test_artist.to_dict())
        assert reponse.status_code == 200
