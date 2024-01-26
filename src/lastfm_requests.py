import json
import requests as re
from typing import Union


def _make_request(request_url: str) -> Union[None, dict]:
    result = re.get(request_url)
    if result.status_code == 200:
        return json.loads(result.content.decode())
    elif result.status_code == 404:
        raise Exception(f"No result returned for {request_url}. Request invalid.")


class LastFMConnection:
    LIBRARY_ARTISTS_ENDPOINT = (
        "http://ws.audioscrobbler.com/2.0/?method=library.getartists"
    )
    ARTIST_INFO_ENDPOINT = "http://ws.audioscrobbler.com/2.0/?method=artist.getinfo"

    def __init__(self, lastfm_api_key: str, lastfm_api_secret: str):
        self.api_key = lastfm_api_key
        self.api_secret = lastfm_api_secret

    def _get_user_artists(
        self,
        user: str,
        limit: int = 5000,
        response_format: str = "json",
    ):
        request_url = "&".join(
            [
                self.LIBRARY_ARTISTS_ENDPOINT,
                f"api_key={self.api_key}",
                f"user={user}",
                f"limit={limit}",
                f"format={response_format}",
            ]
        )
        user_artists = _make_request(request_url)
        return user_artists

    def _get_artist_info(
        self,
        artist_mb_id: Union[None, str] = None,
        artist: Union[None, str] = None,
        response_format: str = "json",
    ):
        if artist_mb_id:
            request_url = "&".join(
                [
                    self.ARTIST_INFO_ENDPOINT,
                    f"api_key={self.api_key}",
                    f"mbid={artist_mb_id}",
                    f"format={response_format}",
                ]
            )
        elif artist:
            request_url = "&".join(
                [
                    self.ARTIST_INFO_ENDPOINT,
                    f"api_key={self.api_key}",
                    f"artist={artist}",
                    f"format={response_format}",
                ]
            )
        artist_info = _make_request(request_url)
        return artist_info
