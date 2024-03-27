
def filter_vacancies(vacancies_list, filter_words):
    filtered_vacancies = []
    for vacancy in vacancies_list:
        if vacancy.description:
            exclude = False
            for word in filter_words:
                if word.lower() in vacancy.title.lower() or word.lower() in vacancy.description.lower():
                    exclude = True
                    break
            if not exclude:
                filtered_vacancies.append(vacancy)
    return filtered_vacancies


def user_interaction():
    platforms = ["HeadHunter"]
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_range = input("Введите диапазон зарплат: ") # Пример: 100000 - 150000

    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)

    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)

    sorted_vacancies = sort_vacancies(ranged_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    print_vacancies(top_vacancies)