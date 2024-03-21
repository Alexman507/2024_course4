from abc import ABC, abstractmethod

import requests


class AbstractAPI(ABC):

    @abstractmethod
    def get_data(self):
        pass


class ServiceAPI(AbstractAPI):
    def __init__(self, url):
        self.url = url

    def get_data(self):
        return requests.get(self.url).json()

    def __repr__(self):
        return f'Получены данные {self.url}'


class Vacancy(ServiceAPI):
    def __init__(self, url):
        super().__init__(url)
        self.data = self.get_data()

    def is_specified(self):
        if self.data['salary'] is None:
            return False

    def compare(self, other):
        if not self.is_specified():
            self.data['salary'] = 'Зарплата не указана'
        return self.data['salary'] > other.data['salary']


class HH(ServiceAPI):
    """
    Класс для работы с API HeadHunter
    Класс Parser является родительским классом, который вам необходимо реализовать
    """

    def __init__(self, file_worker):
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 100}
        self.vacancies = []
        super().__init__(file_worker)

    def load_vacancies(self, keyword):
        self.params['text'] = keyword
        while self.params.get('page') != 20:
            response = requests.get(self.url, headers=self.headers, params=self.params)
            vacancies = response.json()['items']
            self.vacancies.extend(vacancies)
            self.params['page'] += 1