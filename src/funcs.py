import json
from src.vacancy import Vacancy


def init_vacancies_from_json_file(filename) -> list[Vacancy]:
    """Создает экземпляры класса Vacancy из JSON-файла,
    возвращает список.

    """
    with open(filename, 'r', encoding='utf-8') as file:
        vacancies = json.load(file)
        vacancies_list = []
        for item in vacancies:
            vacancy = Vacancy(
                item['_Vacancy__name'],
                item['_Vacancy__url'],
                item['area'],
                item['employer'],
                item['_Vacancy__salary'],
                item['currency'],
                item['requirement']
            )
            vacancies_list.append(vacancy)
    return vacancies_list


def get_vacancies_by_salary(salary: int, currency: str,
                            vacancies) -> list[Vacancy]:
    """Выводит перечень вакансий (объектов класса Vacancy),
    подходящих под указанную з/п

    """
    if salary == 0:
        return vacancies
    chosen_vacancies = []
    for vacancy in vacancies:
        if vacancy.currency == currency and \
                vacancy.salary >= salary:
            chosen_vacancies.append(vacancy)
    sorted_vacancies = sorted(chosen_vacancies, reverse=True)
    return sorted_vacancies


def get_vacancies_by_area(area: str, vacancies) -> list[Vacancy]:
    """Выводит перечень вакансий (объектов класса Vacancy)
    в указанном населенном пункте.

    """
    chosen_vacancies = []
    for vacancy in vacancies:
        if vacancy.area == area:
            chosen_vacancies.append(vacancy)
    return chosen_vacancies


def get_vacancies_by_key_words(key_words: list,
                               vacancies) -> list[Vacancy]:
    """Выводит перечень вакансий (объектов класса Vacancy)
    по нахождению ключевых слов в названии и требованиях вакансии.

    """
    chosen_vacancies = []
    url_list = []
    for vacancy in vacancies:
        for word in key_words:
            if word in vacancy.requirement or word in vacancy.name:
                if vacancy.url not in url_list:
                    url_list.append(vacancy.url)
                    chosen_vacancies.append(vacancy)
    return chosen_vacancies


def salary_scenario(vacancies):
    salary = int(input('Укажите минимальный уровень зарплаты: '))
    currency = (input('Введите код валюты, '
                      'например RUB, USD, KZT: ')).upper()
    vacancies_by_salary = get_vacancies_by_salary(salary,
                                                  currency,
                                                  vacancies)
    common_scenario(vacancies_by_salary)
    return vacancies_by_salary


def common_scenario(vacancies: list[Vacancy]):
    """Общий сценарий обработки запросов пользователя"""
    if vacancies:
        print()
        print(*vacancies, sep='\n\n')
        print()
        print(f'Итого найдено {len(vacancies)} вакансий.\n')
    else:
        print('Нет вакансий, соответствующих заданным критериям. '
              'Программа завершена.')
        return
