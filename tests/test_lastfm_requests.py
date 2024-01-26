import os
import unittest
from dotenv import load_dotenv
from src.lastfm_requests import LastFMConnection


class LastFMConnectionTests(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        api_key = os.getenv("LASTFM_API_KEY")
        api_secret = os.getenv("LASTFM_API_SECRET")
        self.lastfm_connection = LastFMConnection(api_key, api_secret)

    def testLibraryArtists(self):
        cardoor_libary_artists = self.lastfm_connection._get_user_artists(
            "Car_door", limit=10
        )
        self.assertEqual(len(cardoor_libary_artists["artists"]["artist"]), 10)

    def testGetArtistInfo(self):
        artist_info = self.lastfm_connection._get_artist_info(artist="j dilla")
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
            ],
        )

if __name__ == '__main__':
    unittest.main()