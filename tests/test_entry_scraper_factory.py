#  Copyright (c) 2021 Aaron Beetstra
#  All rights reserved.

import unittest

from pokemon_dex_entries.bulbapedia.pokedex_entry_bulbapedia import PokedexEntryBulbapedia
from pokemon_dex_entries.entry_scraper_factory import EntryScraperFactory


class TestEntryScaperFactory(unittest.TestCase):
    def test_type_bulbapedia(self):
        """
        Test whether a PokeDexEntryBulbapedia instance is created provided the correct type is given
        """
        test_source_type = "bulbapedia"
        test_url = "https://bulbapedia.bulbagarden.net/w/index.php?title=Flapple_(Pok%C3%A9mon)&action=edit"

        result = EntryScraperFactory().create(source_type=test_source_type, url=test_url)

        self.assertIsInstance(result, PokedexEntryBulbapedia)

    def test_type_invalid(self):
        """
        Test if a ValueError is thrown if an invalid source type is provided
        """
        test_source_type = "InvalidTestType"
        test_url = "https://InvalidTestTypeStringSomeWebsite"
        scraper_class = EntryScraperFactory()

        self.assertRaises(ValueError, scraper_class.create, source_type=test_source_type, url=test_url)


if __name__ == '__main__':
    unittest.main()
