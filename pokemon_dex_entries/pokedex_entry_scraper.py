#  Copyright (c) 2020 Aaron Beetstra
#  All rights reserved.

import abc

import requests
from bs4 import BeautifulSoup


class PokedexEntryScraper(abc.ABC):

    def __init__(self, url: str):
        request = requests.get(url)
        self.structured_object = BeautifulSoup(request.text, 'html.parser')

    @abc.abstractmethod
    def generate_usable_data(self):
        pass
