from abc import ABC, abstractmethod

import requests


class AbstractAPI(ABC):

    @abstractmethod
    def get_data(self, keyword):
        pass


class HH(AbstractAPI, ABC):
    """
    Класс для работы с API HeadHunter
    """

    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 5}
        self.vacancies = []

    def get_data(self, keyword):
        self.params['text'] = keyword
        while self.params.get('page') != 5:
            response = requests.get(self.url, headers=self.headers, params=self.params)
            vacancies = response.json()['items']
            self.vacancies.extend(vacancies)
            self.params['page'] += 1
        # print(response.status_code)

    def is_specified(self):
        if 'salary' not in self.vacancies:
            return False

    def compare(self, other):
        if not self.is_specified():
            self.vacancies['salary'] = 'Зарплата не указана'
        return self.vacancies['salary'] > other.vacancies['salary']


# g1 = HH()
# v1 = g1.get_data('Разработчик')
# print(g1.vacancies)
