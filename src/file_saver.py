import json
from abc import ABC, abstractmethod


class FileSaver(ABC):

    @abstractmethod
    def add_vacancies(self, filename, vacancies):
        pass

    @abstractmethod
    def delete_vacancy(self, filename, vacancy):
        pass


class JSONSaver(FileSaver):
    """Класс для сохранения полученных по API вакансий
    в json-файл и работы с ними.

    """
    def add_vacancies(self, filename, vacancies_obj: list):
        """Сохраняет вакансии (экземпляры класса `Vacancy`) в файл.
        :param vacancies_obj: Список вакансий в виде словаря Python
        :param filename: файл для записи информации по вакансиям.

        """
        vacancies = []
        for vacancy in vacancies_obj:
            vacancies.append(vacancy.__dict__)

        with open(filename, 'w', encoding='utf-8') as file:
            file.write(
                json.dumps(
                    vacancies,
                    indent=2,
                    ensure_ascii=False
                )
            )

    def delete_vacancy(self, filename, vacancy_id: str):
        """Удаляет вакансию (объект Vacancy) из файла"""

        with open(filename, 'r', encoding='utf-8') as file:
            vacancies = json.load(file)
        edited_vacancies = []
        for vacancy in vacancies:
            if vacancy["_Vacancy__url"].endswith(vacancy_id) or \
                    vacancy["_Vacancy__url"][-13:-5] == vacancy_id:
                continue
            else:
                edited_vacancies.append(vacancy)
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(json.dumps(edited_vacancies,
                                  indent=2,
                                  ensure_ascii=False))
