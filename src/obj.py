import os
from abc import ABC, abstractmethod
import requests
import json


class AbstractAPI(ABC):
    """
    Абстрактный класс для работы с API
    """

    @abstractmethod
    def get_data(self, keyword):
        pass


class HH(AbstractAPI, ABC):
    """
    Класс для работы с API HeadHunter
    """

    def __init__(self, area=113) -> None:
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 5}
        self.vacancies = []
        self.area = area

    def get_data(self, keyword):
        print(f"Поиск вакансий по ключевому слову, пожалуйста подождите...")
        self.params['text'] = keyword
        self.params['area'] = self.area
        while self.params.get('page') != 5:
            response = requests.get(self.url, headers=self.headers, params=self.params)
            vacancies = response.json()['items']
            self.vacancies.extend(vacancies)
            self.params['page'] += 1
        return self.vacancies


class Vacancy:
    """Класс для ваканский, содержит название, работодателя, ссылку на вакансию, описание, требования и зарплату"""

    def __init__(self, name: str, employer: str, url: str, description: str, requirements: str, salary):
        self.name = name
        self.employer = employer
        self.url = url
        self.description = description
        self.requirements = requirements
        self.salary_min = None
        self.salary_max = None
        self.compare_salary(salary)

    def __repr__(self):
        return (f"{self.name}\n"
                f"{self.employer}\n"
                f"{self.salary_min}\n"
                f"{self.salary_max}\n"
                f"{self.description}\n"
                f"{self.url}")

    def __str__(self) -> str:
        return (f"Вакансия: {self.name}\n"
                f"Работодатель: {self.employer}\n"
                f"Заработная плата: {self.get_salary()}\n"
                f"Требования: {self.requirements}\n"
                f"Описание: {self.description}\n"
                f"Ссылка на вакансию: {self.url}\n")

    def __gt__(self, other):
        if isinstance(other, Vacancy):
            if self.salary_min and other.salary_min:
                return self.salary_min > other.salary_min
            else:
                return False

    def __lt__(self, other):
        if isinstance(other, Vacancy):
            if self.salary_min and other.salary_min:
                return self.salary_min < other.salary_min
            else:
                return False

    def get_salary(self):
        if self.salary_min:
            if self.salary_max:
                return f"от {self.salary_min} до {self.salary_max} руб."
            else:
                return f"от {self.salary_min} руб."
        if self.salary_max:
            return f"до {self.salary_max} руб."
        return "данные о заработной плате отсутствуют"

    def compare_salary(self, salary):
        if isinstance(salary, str) and '-' in salary:
            salary_slice = salary.split('-')
            self.salary_min = int(''.join(filter(str.isdigit, salary_slice[0])))
            self.salary_max = int(''.join(filter(str.isdigit, salary_slice[1])))
        elif isinstance(salary, int):
            self.salary_min = salary
            self.salary_max = salary
        elif isinstance(salary, dict):
            self.salary_min = salary.get('from')
            self.salary_max = salary.get('to')
        else:
            self.salary_min = None
            self.salary_max = None


class AbstractFile(ABC):
    """
        Абстрактный класс для работы с файлами
    """

    @abstractmethod
    def add_data_to_dict(self, vacancy: Vacancy):  # Запись
        pass

    @abstractmethod
    def get_data(self):  # Чтение
        pass

    @abstractmethod
    def del_data_dict(self):  # Удаление
        pass


class JSONFile(AbstractFile, ABC):
    """Класс для работы с файлом JSON (Чтение, запись, удаление)"""

    def __init__(self, filename: str):
        self.filename = filename

    def add_data_to_dict(self, vacancy: Vacancy):
        with open(self.filename, 'a', encoding='UTF-8') as file:
            json.dump(vacancy.__dict__, file, ensure_ascii=False, indent=4)
            file.write('\n')

    def get_data(self):
        with open(self.filename, 'r', encoding='UTF-8') as file:
            vacancies = [json.loads(line) for line in file.readlines()]
        return vacancies

    def del_data_dict(self):
        open(self.filename, 'w').close()
