from pathlib import Path
import json
from abc import ABC, abstractmethod
from src.vacancy import Vacancy


ROOT_PATH = Path(__file__).parent
PATH_TO_FILE = Path.joinpath(ROOT_PATH, "vacancies.json")


class FileSaver(ABC):

    @abstractmethod
    def add_vacancies(self, vacancies):
        pass

    @abstractmethod
    def get_vacancies_by_salary(self, salary, currency):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy):
        pass


class JSONSaver(FileSaver):
    """
    Класс для сохранения полученных по API вакансий
    в json-файл и работы с ними.
    """

    def add_vacancies(self, vacancies_obj: list):
        """Сохраняет вакансии (экземпляры класса `Vacancy`) в файл.
        :param vacancies_obj: Список вакансий в виде словаря Python.
        """
        vacancies = []
        for vacancy in vacancies_obj:
            vacancies.append(vacancy.__dict__)

        with open(PATH_TO_FILE, 'w', encoding='utf-8') as file:
            file.write(
                json.dumps(
                    vacancies,
                    indent=2,
                    ensure_ascii=False
                )
            )

    @staticmethod
    def init_vacancies_from_file(file=PATH_TO_FILE):
        """Создает экземпляры класса Vacancy из JSON-файла,
        возвращает список"""
        with open(file, 'r', encoding='utf-8') as file:
            vacancies = json.load(file)
            vacancies_list = []
            for item in vacancies:
                vacancy = Vacancy(
                    item['name'],
                    item['url'],
                    item['salary'],
                    item['currency'],
                    item['requirement']
                )
                vacancies_list.append(vacancy)
        return vacancies_list

    def get_vacancies_by_salary(self, salary: int, top_n: int, currency='RUR'):
        """Выводит перечень вакансий (объектов класса Vacancy),
        подходящих под указанную з/п"""
        vacancies = self.init_vacancies_from_file()
        chosen_vacancies = []
        for vacancy in vacancies:
            if vacancy.currency == currency:
                if vacancy.salary >= salary:
                    chosen_vacancies.append(vacancy)
        if not chosen_vacancies:
            print('Нет вакансий, соответствующих заданным критериям.')
        else:
            sorted_vacancies = sorted(chosen_vacancies, reverse=True)
            print(*sorted_vacancies[:top_n], sep='\n\n')

    def delete_vacancy(self, vacancy):
        pass
