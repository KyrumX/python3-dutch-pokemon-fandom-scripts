#  Copyright (c) 2020 Aaron Beetstra
#  All rights reserved.

import argparse

from pokemon_dex_entries.entry_scraper_factory import EntryScraperFactory


def main():
    parser = argparse.ArgumentParser(description='Scrape a website and convert the data to a Pokémon entry using a '
                                                 'format usable by the Dutch Pokémon fandom/.')

    parser.add_argument('-url', action="store", help='Target url', required=True)
    parser.add_argument('-type', action="store", help='Source type of website being scraped, options', type=str,
                        choices=["bulbapedia"], default="bulbapedia")

    args = parser.parse_args()

    # scraper_class = EntryScraperFactory().create(source_type="bulbapedia", url="https://bulbapedia.bulbagarden.net/w/index.php?title=Pikachu_(Pok%C3%A9mon)&action=edit")
    scraper_class = EntryScraperFactory().create(source_type=args.type, url=args.url)

    try:
        dutch_format = scraper_class.build_template()

        text_file = open("output.txt", "w", encoding='utf8')
        text_file.write(dutch_format)
        text_file.close()

        print("Done! Dutch Fandom formatted text can be found in output.txt")

    except Exception as e:
        print("Something went wrong during scraping, the source site may have changed its format.")


if __name__ == "__main__":
    main()
