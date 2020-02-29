from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup


class ListScraper(ABC):

    def __init__(self, url: str):
        request = requests.get(url)
        self.structured_object = BeautifulSoup(request.text, 'html.parser')

    @abstractmethod
    def scrape(self):
        pass
