import requests
from abc import ABC, abstractmethod
import os
import pprint
from time import sleep


class BaseAPI(ABC):

    @abstractmethod
    def get_vacancies(self, key_word):
        pass


class HeadHunterAPI(BaseAPI):
    """Класс для API сайта hh.ru"""

    url = "https://api.hh.ru/"

    def get_vacancies(self, key_word) -> list[dict]:
        """Посылает запрос к API hh.ru,
        получает перечень вакансий, содержащих в описании ключевое слово/слова,
        преобразует JSON-данные в словарь Python.
        :param key_word: Ключевое слово/слова.
        :return: Список вакансий.

        """
        vacancies_list = []
        for page in range(2):
            params = {
                'text': key_word,
                'page': page,
                'per_page': 10,
            }
            response = requests.get(self.url + 'vacancies/', params)
            if not response.ok:
                print(f'Ошибка {response}')
            else:
                data = response.json()
                vacancies_list.extend(data['items'])
                sleep(2)
        return vacancies_list

    def get_vacancy_by_id(self, id):
        """Направляет запрос по API hh.ru с указанием id вакансии,
        получает полное описание вакансии в формате словаря Python.

        """
        response = requests.get(self.url + 'vacancies/' + id)
        if not response.ok:
            print(f'Ошибка {response}')
        else:
            data = response.json()
            pprint.pprint(data)


class SuperJobAPI(BaseAPI):
    """Класс для API сайта superjob.ru"""

    sj_api_key: str = os.getenv('SJ_API_KEY')
    url = "https://api.superjob.ru/2.0/"

    def get_vacancies(self, key_word) -> list[dict]:
        """Посылает запрос к API superjob.ru,
        получает перечень вакансий, содержащих в описании ключевое слово/слова,
        преобразует JSON-данные в словарь Python.

        """
        vacancies_list = []
        for page in range(2):
            headers = {'X-Api-App-Id': self.sj_api_key}
            params = {
                'keyword': key_word,
                'page': page,
                'count': 10,
            }
            response = requests.get(self.url + 'vacancies/',
                                    headers=headers,
                                    params=params)
            if not response.ok:
                print(f'Ошибка {response}')
            else:
                data = response.json()
                vacancies_list.extend(data['objects'])
                sleep(2)
        return vacancies_list

    def get_vacancy_by_id(self, id):
        """Направляет запрос по API superjob.ru с указанием
        id вакансии, получает полное описание вакансии
        в формате словаря Python

        """
        headers = {'X-Api-App-Id': self.sj_api_key}
        response = requests.get(self.url + 'vacancies/' + id,
                                headers=headers)
        if not response.ok:
            print(f'Ошибка {response}')
        else:
            data = response.json()
            pprint.pprint(data)
