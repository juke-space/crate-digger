import numpy as np
from typing import Union, List
from src.efficient_requests import make_request, send_async_requests


class LastFMCollector:
    LIBRARY_ARTISTS_ENDPOINT = (
        "http://ws.audioscrobbler.com/2.0/?method=library.getartists"
    )
    ARTIST_INFO_ENDPOINT = "http://ws.audioscrobbler.com/2.0/?method=artist.getinfo"
    MUSIC_BRAINZ_ID_FIELD = "mbid"
    NAME_FIELD = "name"
    ARTIST_FIELD = "artist"
    MAX_CONCURRENT_REQUESTS = 100

    def __init__(self, lastfm_api_key: str, lastfm_api_secret: str):
        self.api_key = lastfm_api_key
        self.api_secret = lastfm_api_secret

    def get_library_artist_info(self, username: str, limit: int = 1000):
        library_artist_results = self._get_user_artists(username, limit=limit)
        artist_names = [
            artist_dict[self.NAME_FIELD]
            for artist_dict in library_artist_results["artists"][self.ARTIST_FIELD]
        ]
        library_artist_info_results = self._get_artists_info_async(artist_names=artist_names)
        return library_artist_info_results

    def _get_user_artists(
        self,
        user: str,
        limit: int,
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
        user_artists = make_request(request_url)
        return user_artists

    def _get_artist_info(
        self,
        artist_mbid: Union[None, str] = None,
        artist_name: Union[None, str] = None,
        response_format: str = "json",
    ):
        if artist_mbid:
            request_url = self._construct_artist_query(
                self.MUSIC_BRAINZ_ID_FIELD, artist_mbid, response_format
            )
        elif artist_name:
            request_url = self._construct_artist_query(
                self.ARTIST_FIELD, artist_name, response_format
            )
        artist_info = make_request(request_url)
        return artist_info

    def _get_artists_info_async(  # NOTE: Make this take a list of artists rather than a single one.
        self,
        artist_mbids: Union[None, List[str]] = None,
        artist_names: Union[None, List[str]] = None,
        response_format: str = "json",
    ):
        num_mbid_queries = len(artist_mbids) if artist_mbids else 0
        num_name_queires = len(artist_names) if artist_names else 0
        query_urls = np.empty(num_mbid_queries + num_name_queires, dtype=object)

        if num_mbid_queries:
            query_urls[:num_mbid_queries] = np.array(
                [
                    self._construct_artist_query(
                        self.MUSIC_BRAINZ_ID_FIELD, artist_mbid, response_format
                    )
                    for artist_mbid in artist_mbids
                ]
            )
        if num_name_queires:
            query_urls[:num_name_queires] = np.array(
                [
                    self._construct_artist_query(
                        self.ARTIST_FIELD, artist_name, response_format
                    )
                    for artist_name in artist_names
                ]
            )
        return send_async_requests(query_urls, self.MAX_CONCURRENT_REQUESTS)

    def _construct_artist_query(
        self, id_field: str, id_value: str, response_format: str
    ):
        return "&".join(
            [
                self.ARTIST_INFO_ENDPOINT,
                f"api_key={self.api_key}",
                f"{id_field}={id_value}",
                f"format={response_format}",
            ]
        )
