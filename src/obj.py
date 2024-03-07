from abc import ABC, abstractmethod

import requests


class AbstractAPI(ABC):

    @abstractmethod
    def get_data(self):
        pass


class ServiceAPI(AbstractAPI, ABC):
    def __init__(self, url):
        self.url = url

    def get_data(self):
        return requests.get(self.url).json()

    def __repr__(self):
        return self.url