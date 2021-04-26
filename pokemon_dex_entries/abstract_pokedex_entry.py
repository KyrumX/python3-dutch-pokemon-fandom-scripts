#  Copyright (c) 2021 Aaron Beetstra
#  All rights reserved.
import abc


class AbstractPokedexEntry(abc.ABC):
    """
    Abstract Pokedex Entry class

    Used to define the source for our template
    """

    @abc.abstractmethod
    def setup(self):
        pass

    @abc.abstractmethod
    def build_template(self):
        pass
