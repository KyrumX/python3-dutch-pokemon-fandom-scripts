from pokemon_lists.list_scraper_serebii import ListScraperSerebii


class ListScraperFactory():
    @classmethod
    def create(cls, source_type: str, url: str):
        SOURCE_TYPE_TO_CLASS_MAP = {
            'serebii': ListScraperSerebii,
        }

        if source_type not in SOURCE_TYPE_TO_CLASS_MAP:
            raise ValueError('Invalid source type {}'.format(source_type))

        return SOURCE_TYPE_TO_CLASS_MAP[source_type](url)