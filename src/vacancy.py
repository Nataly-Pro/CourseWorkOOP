class Vacancy:
    """Класс для представления определенных полей вакансии"""

    def __init__(self, name, url, salary, currency, requirement) -> None:
        self.__check(name, url, salary)

        self.name = name
        self.url = url
        self.salary = salary
        self.currency = currency
        self.requirement = requirement

    @staticmethod
    def __check(name, url, salary):
        if not isinstance(name, str):
            raise TypeError('Должна быть строка.')
        if not isinstance(salary, int) and salary != 'не указана':
            raise TypeError('Должно быть целое число.')
        if not isinstance(url, str) and not url.startswith('https://'):
            raise TypeError('Ссылка на вакансию должна быть строкой '
                            'и начинаться на "https://".')

    @classmethod
    def init_from_hh_data(cls, hh_data: list[dict]):
        """Класс - метод, инициализирующий экземпляры класса
        `Vacancy` данными о вакансиях, полученными с сайта hh.ru.
        :param hh_data: Список вакансий в виде словаря Python.
        """
        vacancies_list = []
        for vacancy in hh_data:
            name = vacancy['name']
            url = vacancy['url']
            requirement = vacancy['snippet']['requirement']

            if vacancy['salary'] is None:
                salary = 'не указана'
                currency = ''
            else:
                currency = vacancy['salary']['currency']

                if vacancy['salary']['from'] is None:
                    salary = vacancy['salary']['to']
                else:
                    salary = vacancy['salary']['from']

            vacancy_obj = cls(name, url, salary, currency, requirement)
            vacancies_list.append(vacancy_obj)
        return vacancies_list

    def __str__(self):
        return f'{self.name}\n' \
               f'{self.url}\n' \
               f'{self.salary} {self.currency}\n' \
               f'{self.requirement}'

    def __lt__(self, other):
        """
        Метод сравнения вакансий между собой по зарплате.
        Возвращает результат сравнения (True/False).
        """
        return self.salary < other.salary

