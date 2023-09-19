import re


class Vacancy:
    """Класс для представления определенных полей вакансии"""

    def __init__(self, name, url, area, employer, salary,
                 currency, requirement) -> None:
        self.__check(name, url, salary)

        self.__name = name
        self.__url = url
        self.area = area
        self.employer = employer
        self.__salary = salary
        self.currency = currency
        self.requirement = requirement

    @property
    def name(self):
        return self.__name

    @property
    def url(self):
        return self.__url

    @property
    def salary(self):
        return self.__salary

    @staticmethod
    def __check(name, url, salary):
        if not isinstance(name, str):
            raise TypeError('Должна быть строка.')
        if not isinstance(salary, int):
            raise TypeError('Должно быть целое число.')
        if not isinstance(url, str) and not url.startswith('https://'):
            raise TypeError('Ссылка на вакансию должна быть строкой '
                            'и начинаться на "https://".')

    @classmethod
    def init_from_hh_data(cls, hh_data: list[dict]) -> list['Vacancy']:
        """Класс - метод, инициализирующий экземпляры класса
        `Vacancy` данными о вакансиях, полученными с сайта hh.ru.
        :param hh_data: Список вакансий в виде словаря Python.

        """
        vacancies_list = []
        for vacancy in hh_data:
            name = vacancy['name']
            url = vacancy['alternate_url']
            area = vacancy['area']['name']
            employer = f"Работодатель: {vacancy['employer']['name']}"
            if vacancy['snippet']['requirement'] is None:
                requirement = 'Требования не указаны.'
            else:
                req = re.sub('</?highlighttext>', '',
                             vacancy['snippet']['requirement'])
                requirement = f"Требования: {req}"

            if vacancy['salary'] is None or \
                    vacancy['salary']['from'] is None:
                salary = 0
                currency = ''
            else:
                salary = vacancy['salary']['from']
                if vacancy['salary']['currency'] == 'RUR':
                    currency = 'RUB'
                else:
                    currency = vacancy['salary']['currency']

            vacancy_obj = cls(name, url, area, employer,
                              salary, currency, requirement)
            vacancies_list.append(vacancy_obj)
        return vacancies_list

    @classmethod
    def init_from_sj_data(cls, sj_data: list[dict]):
        """Класс - метод, инициализирующий экземпляры класса
        `Vacancy` данными о вакансиях, полученными с сайта superjob.ru.
        :param sj_data: Список вакансий в виде словаря Python.

        """
        vacancies_list = []
        for vacancy in sj_data:
            name = vacancy['profession']
            url = vacancy['link']
            area = vacancy['town']['title']
            employer = f"Работодатель: {vacancy['firm_name']}"
            currency = vacancy['currency'].upper()
            requirement = vacancy['candidat']
            salary = vacancy['payment_from']

            vacancy_obj = cls(name, url, area, employer,
                              salary, currency, requirement)
            vacancies_list.append(vacancy_obj)
        return vacancies_list

    def __str__(self):
        return f'{self.name}\n' \
               f'{self.url}\n' \
               f'{self.area}\n' \
               f'{self.employer}\n' \
               f'{self.salary} {self.currency}\n' \
               f'{self.requirement}'

    def __lt__(self, other):
        """
        Метод сравнения вакансий между собой по зарплате.
        Возвращает результат сравнения (True/False).

        """
        return self.salary < other.salary
