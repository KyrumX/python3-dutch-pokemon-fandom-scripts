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

    def setUp(self) -> None:
        """
        Create a test instance, so that we don't need to create a new one every test
        """
        self.test_url = "https://bulbapedia.bulbagarden.net/w/index.php?title=Rockruff_(Pok%C3%A9mon)&action=edit"
        self.test_scraper = PokedexEntryScraperPokemonBulbapedia(self.test_url)

    def test_init_url_set(self):
        """
        Test whether the url is correctly set during initializing
        """
        self.assertEqual(self.test_scraper.url, self.test_url)

    def test_init_structured_object_is_none(self):
        """
        Test whether the structured_object is None after initializing
        """
        self.assertEqual(self.test_scraper.structured_object, None)

    @mock.patch("pokemon_dex_entries.pokedex_entry_scraper.requests.get", side_effect=mocked_get_request)
    def test_mocked_get_structured_object(self, mocked_get):
        """
        Test whether the structured_object is correctly set using BeautifulSoup
        Mocked the requests.get to a local file
        """
        self.test_scraper.get_structured_object()

        with open(generate_test_file_path(), 'rb') as html:
            expected_soup = BeautifulSoup(html, 'html.parser')
            self.assertEqual(self.test_scraper.structured_object, expected_soup)

    def test_generating_of_data(self):
        """
        Test whether the usable data is correctly generated
        This one is not mocked, uses live data
        """

        # First run .get_structured_object() to retrieve said data
        self.test_scraper.get_structured_object()

        # The results we expect
        expected_infobox = {'name': 'Rockruff', 'jname': 'イワンコ', 'tmname': 'Iwanko', 'form2': 'Event', 'ndex': '744', 'type1': 'Rock', 'category': 'Puppy', 'height-ftin': '1\'08"', 'height-m': '0.5', 'weight-lbs': '20.3', 'weight-kg': '9.2', 'abilitylayout': '2+1', 'abilitycold': '2', 'ability1': 'Keen Eye', 'ability2': 'Vital Spirit', 'abilityd': 'Steadfast', 'ability2-1': 'Own Tempo', 'egggroupn': '1', 'egggroup1': 'Field', 'eggcycles': '15', 'evtotal': '1', 'evat': '1', 'expyield': '56', 'lv100exp': '1,000,000', 'gendercode': '127', 'color': 'Brown', 'catchrate': '190', 'body': '08', 'pokefordex': 'rockruff', 'generation': '7', 'friendship': '70'}
        expected_prev_next = {'type': 'Rock', 'prevnum': '743', 'prev': 'Ribombee', 'nextnum': '745', 'next': 'Lycanroc', 'roundleft': 'tl', 'roundright': 'tr'}
        expected_raw_evo_lines = ['/1branch2|type1=Rock|no1=744|name1=Rockruff|type1-1=Rock|evo1a={{bag|Rare Candy}} [[File:HOME Sun icon.png|24px|Pokémon Sun|link=Pokémon Sun and Moon]][[File:HOME Ultra Sun icon.png|24px|Pokémon Ultra Sun|link=Pokémon Ultra Sun and Ultra Moon]]<br>Level 25<br><small>during the {{color2|000|time|day}}<br>in {{color2|000|Pokémon Sun and Moon|Pokémon Sun}}<br>or {{color2|000|Pokémon Ultra Sun and Ultra Moon|Ultra Sun}}|no2a=745|name2a=Lycanroc|form2a=Midday Form|type1-2a=Rock|evo1b={{bag|Rare Candy}} [[File:HOME Moon icon.png|24px|Pokémon Sun|link=Pokémon Sun and Moon]][[File:HOME Ultra Moon icon.png|24px|Pokémon Ultra Sun|link=Pokémon Ultra Sun and Ultra Moon]]<br>Level 25<br><small>at {{color2|000|time|night}}<br>in {{color2|000|Pokémon Sun and Moon|Pokémon Moon}}<br>or {{color2|000|Pokémon Ultra Sun and Ultra Moon|Ultra Moon}}|no2b=745|art2b=745Lycanroc-Midnight|name2b=Lycanroc|form2b=Midnight Form|type1-2b=Rock', '-2|pictype=sprite|type1=Rock|no1=744Rockruff|name1=Rockruff|type1-1=Rock|evo1={{bag|Rare Candy}} + {{bag|Ability Urge}}<br>{{color2|000|Level|Level 25}}<br><small>between {{color2|000|time|5:00<br>and 5:59 PM}} in-game<br>if its {{color2|000|Ability}} is {{acolor|Own Tempo|000}}</small>|no2=745Lycanroc-Dusk|name2=Lycanroc|type1-2=Rock', '/1branch2|type1=Rock|no1=744|name1=Rockruff|type1-1=Rock|evo1a={{bag|Rare Candy}}<br>Level 25<br><small>during the {{color2|000|time|day}}|no2a=745|name2a=Lycanroc|form2a=Midday Form|type1-2a=Rock|evo1b={{bag|Rare Candy}}<br>Level 25<br><small>at {{color2|000|time|night}}|no2b=745|art2b=745Lycanroc-Midnight|name2b=Lycanroc|form2b=Midnight Form|type1-2b=Rock', '-2|pictype=sprite|type1=Rock|no1=744Rockruff|name1=Rockruff|type1-1=Rock|evo1={{bag|Rare Candy}} + {{bag|Ability Urge}}<br>{{color2|000|Level|Level 25}}<br><small>between {{color2|000|time|7:00<br>and 7:59 PM}} real-time<br>if its {{color2|000|Ability}} is {{acolor|Own Tempo|000}}</small>|no2=745Lycanroc-Dusk|name2=Lycanroc|type1-2=Rock']
        expected_forms = {}
        expected_local_dex = {'Alola': ['103', '126'], 'Galar': ['157']}
        r_infobox, r_prev_next, r_raw_evo_lines, r_forms, r_local_dex = self.test_scraper.generate_usable_data()

        # Assert the end values
        self.assertEqual(r_infobox, expected_infobox)
        self.assertEqual(r_prev_next, expected_prev_next)
        self.assertEqual(r_raw_evo_lines, expected_raw_evo_lines)
        self.assertEqual(r_forms, expected_forms)
        self.assertEqual(r_local_dex, expected_local_dex)


if __name__ == '__main__':
    unittest.main()
