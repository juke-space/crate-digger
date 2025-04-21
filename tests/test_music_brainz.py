from crate_server.models.artist_query import ArtistQuery
from music_brainz import get_artists_by_location


def test_get_artists_by_location():
    limit = 10
    query = ArtistQuery(municipality="Hartford", state_province="Connecticut", country="USA", limit=limit)
    results = get_artists_by_location(query)
    assert len(results) == limit
