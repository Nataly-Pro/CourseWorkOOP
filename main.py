from src.api_classes import HeadHunterAPI, SuperJobAPI
from src.vacancy import Vacancy
from src.file_saver import JSONSaver
from src.funcs import get_vacancies_by_area, common_scenario, \
    get_vacancies_by_key_words, init_vacancies_from_json_file, salary_scenario
from settings import PATH_TO_HH_FILE, PATH_TO_SJ_FILE


def user_interaction():
    hh_api = HeadHunterAPI()
    sj_api = SuperJobAPI()

    platform_number = input('Выберите номер платформы для поиска вакансий: '
                            '1- "HeadHunter" или 2- "SuperJob": ')
    key_word = input('Введите поисковый запрос: ')

    if platform_number == '1':
        hh_data = hh_api.get_vacancies(key_word)
        vacancies_obj_list = Vacancy.init_from_hh_data(hh_data)
        file = PATH_TO_HH_FILE

    elif platform_number == '2':
        sj_data = sj_api.get_vacancies(key_word)
        vacancies_obj_list = Vacancy.init_from_sj_data(sj_data)
        file = PATH_TO_SJ_FILE

    else:
        print('Не указан номер платформы, программа завершена.')
        return

    json_saver = JSONSaver()
    json_saver.add_vacancies(file, vacancies_obj_list)
    vacancies = init_vacancies_from_json_file(file)

    user_first_choice = input('Выберите, по какому свойству '
                              'отсортировать найденные вакансии:\n'
                              '1. по зарплате,\n'
                              '2. по городу,\n'
                              '3. по ключевому слову/словам,\n'
                              'Ваш выбор: ')

    if user_first_choice == '1':
        vacancies_by_salary = salary_scenario(vacancies)
        json_saver.add_vacancies(file, vacancies_by_salary)

        user_input = input('Желаете продолжить работу с вакансиями? '
                           '(Да/Нет): ').lower()
        if user_input == 'да':
            user_second_choice = input('Выберите, по какому свойству '
                                       'отсортировать выбранные вакансии:\n'
                                       '1. по городу\n'
                                       '2. по ключевому слову/словам\n'
                                       '3. по id\n'
                                       'Ваш выбор: ')

            if user_second_choice == '1':
                area = input('Укажите город: ').title()

                vacancies_by_area = get_vacancies_by_area(
                    area,
                    vacancies_by_salary)
                common_scenario(vacancies_by_area)
                json_saver.add_vacancies(file, vacancies_by_area)

                user_third_choice = input('Отсортировать выбранные '
                                          'вакансии по ключевому '
                                          'слову/словам? (Да/Нет): ')

                if user_third_choice == 'да':
                    key_words = input('Введите ключевые слова для '
                                      'фильтрации вакансий: ').split()

                    vacancies_by_key = get_vacancies_by_key_words(
                        key_words,
                        vacancies_by_area)
                    common_scenario(vacancies_by_key)
                    json_saver.add_vacancies(file, vacancies_by_key)

                    user_fourth_choice = input(
                        'Показать полный вид вакансии по '
                        'определенному id? (Да/Нет): ')

                    if user_fourth_choice == 'да':
                        vacancy_id = input('Введите id-номер вакансии '
                                           '(8 цифр в ссылке): ')

                        if platform_number == '1':
                            hh_api.get_vacancy_by_id(vacancy_id)
                        elif platform_number == '2':
                            sj_api.get_vacancy_by_id(vacancy_id)
                        return

            if user_second_choice == '2':
                key_words = input('Введите ключевые слова '
                                  'для фильтрации вакансий: ').split()

                vacancies_by_key = get_vacancies_by_key_words(
                    key_words,
                    vacancies_by_salary)
                common_scenario(vacancies_by_key)
                json_saver.add_vacancies(file, vacancies_by_key)

                user_third_choice = input('Выбрать вакансии по городу? '
                                          '(Да/Нет): ')

                if user_third_choice == 'да':
                    area = input('Укажите город: ').title()

                    vacancies_by_area = get_vacancies_by_area(area,
                                                              vacancies_by_key)
                    print()
                    common_scenario(vacancies_by_area)
                    json_saver.add_vacancies(file, vacancies_by_area)
                    return

            if user_second_choice == '3':
                vacancy_id = input('Введите id-номер вакансии '
                                   '(8 цифр в ссылке): ')
                print()
                if platform_number == '1':
                    hh_api.get_vacancy_by_id(vacancy_id)
                elif platform_number == '2':
                    sj_api.get_vacancy_by_id(vacancy_id)
                return

    if user_first_choice == '2':
        area = input('Укажите город: ').title()

        vacancies_by_area = get_vacancies_by_area(area, vacancies)
        common_scenario(vacancies_by_area)
        json_saver.add_vacancies(file, vacancies_by_area)

        user_second_choice = input('Отсортировать выбранные вакансии '
                                   'по зарплате? (Да/Нет): ')

        if user_second_choice == 'да':
            vacancies_by_salary = salary_scenario(vacancies_by_area)
            json_saver.add_vacancies(file, vacancies_by_salary)
            return

    if user_first_choice == '3':
        key_words = input('Введите ключевые слова '
                          'для фильтрации вакансий: ').split()

        vacancies_by_key = get_vacancies_by_key_words(key_words, vacancies)
        common_scenario(vacancies_by_key)
        json_saver.add_vacancies(file, vacancies_by_key)

        user_second_choice = input('Отсортировать выбранные вакансии '
                                   'по зарплате? (Да/Нет): ')

        if user_second_choice == 'да':
            vacancies_by_salary = salary_scenario(vacancies_by_key)
            json_saver.add_vacancies(file, vacancies_by_salary)
            return
    else:
        print('Программа завершена.')
        return


if __name__ == "__main__":
    user_interaction()
