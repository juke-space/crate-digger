from typing import Union, List
from src.efficient_requests import send_async_requests


# Configuration
BASE_API_URL = "https://musicbrainz.org/ws/2/"

MBID_TAG = "<MBID>"
INCLUDED_FIELDS_TAG = "<INC>"
ENTITY_TAG = "<ENTITY_NAME"
ARTIST_NAME_TAG = "<ARTIST_NAME>"

MUSIC_BRAINZ_ID_FIELD = "mbid"
ARTIST_ENTITY_NAME = "artist"

LOOKUP_ENDPOINT = f"/{ENTITY_TAG}/{MBID_TAG}?inc={INCLUDED_FIELDS_TAG}"
SEARCH_ENDPOINT = f"/{ENTITY_TAG}/?query={ARTIST_NAME_TAG}"

MAX_CONCURRENT_REQUESTS = 50


class MusicBrainzCollector:
    def __init__(self, user_agent_str: str) -> None:
        self.user_agent_str = user_agent_str

    def get_artists(
        self,
        artist_names: Union[List[str], None],
        artist_mbids: Union[List[str], None],
        fields_to_include: List[str],
    ):
        artist_search_urls = []
        if artist_names:
            pass
        artist_mbid_urls = []
        if artist_mbids:
            [
                BASE_API_URL
                + LOOKUP_ENDPOINT.replace(ENTITY_TAG, ARTIST_ENTITY_NAME)
                .replace(MBID_TAG, mbid)
                .replace(INCLUDED_FIELDS_TAG, "+".join(fields_to_include))
                for mbid in artist_mbids
            ]
        request_urls = artist_mbid_urls + artist_search_urls
        return send_async_requests(request_urls, MAX_CONCURRENT_REQUESTS) # NOTE: UPDATE TO TAKE COLLECTOR TYPE.
                                                                          # This wil require refactoring the lastfm module a bit.
                                                                          # Don't go over board
