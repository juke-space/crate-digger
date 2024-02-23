import os
import unittest

from dotenv import load_dotenv

from src.lastfm_requests import LastFMCollector


class LastFMCollectorTests(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        api_key = os.getenv("LASTFM_API_KEY")
        api_secret = os.getenv("LASTFM_API_SECRET")
        self.lastfm_connection = LastFMCollector(api_key, api_secret)
        self.username = "Car_door"

    def testLibraryArtists(self):
        cardoor_libary_artists = self.lastfm_connection._get_user_artists(
            self.username, limit=10
        )

        self.assertEqual(len(cardoor_libary_artists["artists"]["artist"]), 10)

    def testGetArtistInfo(self):
        artist_info = self.lastfm_connection._get_artist_info(artist_name="j dilla")
        self.assertEqual(
            (list(artist_info["artist"].keys())),
            [
                "name",
                "mbid",
                "url",
                "image",
                "streamable",
                "ontour",
                "stats",
                "similar",
                "tags",
                "bio",
            ]
        )

    def testGetLibraryArtistInfo(self):
        library_artist_info = self.lastfm_connection.get_library_artist_info(self.username, limit=100)
        self.assertTrue(len(library_artist_info) == 100)


if __name__ == '__main__':
    unittest.main()
