#  Copyright (c) 2021 Aaron Beetstra
#  All rights reserved.
import os
import unittest
from unittest import mock

from bs4 import BeautifulSoup

from pokemon_dex_entries.bulbapedia.pokedex_entry_scraper_bulbapedia import PokedexEntryScraperPokemonBulbapedia


def generate_test_file_path():
    script_dir = os.path.dirname(__file__)
    rel_path = "resources/Rockruff_Test_Page.html"
    abs_file_path = os.path.join(script_dir, rel_path)
    return abs_file_path


def mocked_get_request(*args, **kwargs):
    class MockHtmlResponse:

        @property
        def text(self):
            with open(generate_test_file_path(), 'rb') as html_file:
                html = html_file.read()
            return html

    # Args[0] is equal to self.url in get_structured_object
    if args[0] == "https://bulbapedia.bulbagarden.net/w/index.php?title=Rockruff_(Pok%C3%A9mon)&action=edit":
        return MockHtmlResponse()


class TestPokedexEntryScraperPokemonBulbapedia(unittest.TestCase):
    def test_init_url_set(self):
        """
        Test whether the url is correctly set during initializing
        """
        test_url = "https://bulbapedia.bulbagarden.net/w/index.php?title=Rockruff_(Pok%C3%A9mon)&action=edit"
        test_scraper = PokedexEntryScraperPokemonBulbapedia(test_url)

        self.assertEqual(test_scraper.url, test_url)

    def test_init_structured_object_is_none(self):
        """
        Test whether the structured_object is None after initializing
        """
        test_url = "https://bulbapedia.bulbagarden.net/w/index.php?title=Rockruff_(Pok%C3%A9mon)&action=edit"
        test_scraper = PokedexEntryScraperPokemonBulbapedia(test_url)

        self.assertEqual(test_scraper.structured_object, None)

    @mock.patch("pokemon_dex_entries.pokedex_entry_scraper.requests.get", side_effect=mocked_get_request)
    def test_get_structured_object(self, mocked_get):
        """
        Test whether the structured_object is correctly set using BeautifulSoup
        Mocked the requests.get to a local file
        """
        test_url = "https://bulbapedia.bulbagarden.net/w/index.php?title=Rockruff_(Pok%C3%A9mon)&action=edit"
        test_scraper = PokedexEntryScraperPokemonBulbapedia(test_url)

        test_scraper.get_structured_object()

        with open(generate_test_file_path(), 'rb') as html:
            expected_soup = BeautifulSoup(html, 'html.parser')
            self.assertEqual(test_scraper.structured_object, expected_soup)


if __name__ == '__main__':
    unittest.main()
