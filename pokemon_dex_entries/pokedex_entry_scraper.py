#  Copyright (c) 2020 Aaron Beetstra
#  All rights reserved.

import abc

import requests
from bs4 import BeautifulSoup


class PokedexEntryScraper(abc.ABC):

    def __init__(self, url: str):
        self.url = url
        self.structured_object = None

    def get_structured_object(self):
        request = requests.get(self.url)
        self.structured_object = BeautifulSoup(request.text, "html.parser")

    @abc.abstractmethod
    def generate_usable_data(self):
        pass
