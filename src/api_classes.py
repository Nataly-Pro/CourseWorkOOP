from abc import ABC, abstractmethod
import requests


class BaseAPI(ABC):

    @abstractmethod
    def get_vacancies(self, key_word):
        pass


class HeadHunterAPI(BaseAPI):
    """Класс для API сайта hh.ru"""
    def __init__(self):
        self.url = "https://api.hh.ru/vacancies"

    def get_vacancies(self, key_word='Python') -> list[dict]:
        """
        Посылает запрос к API hh.ru,
        получает перечень вакансий, содержащих в описании ключевое слово,
        преобразует JSON-данные в словарь Python.
        :param key_word: Ключевое слово.
        :return: Список вакансий.
        """
        vacancies_list = []
        for page in range(20):
            params = {
                'text': key_word,
                'page': page,
                'per_page': 100,
            }
            response = requests.get(self.url, params)
            if not response.ok:
                print('Что-то пошло не так. Не удалось установить соединение')
            else:
                data = response.json()
                vacancies_list.extend(data['items'])
        return vacancies_list


class SuperJobAPI(BaseAPI):
    """Класс для API сайта superjob.ru"""
    def __init__(self):
        self.url = "https://api.superjob.ru/2.0/vacancies/"

    def get_vacancies(self, key_word='Python') -> list[dict]:
        pass
