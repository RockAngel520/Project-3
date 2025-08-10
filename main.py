from src.db_manager import DBManager
from src.utils import create_database, create_tables, insert_employers, insert_vacancies


def main():
    """Главная функция"""
    db_name = "project3"
    create_database(db_name)
    create_tables(db_name)
    insert_employers(db_name)
    insert_vacancies(db_name)
    db_manager = DBManager(db_name)

    while True:
        print("\nМЕНЮ:")
        print("1. Показать список компаний и количество вакансий у каждой компании")
        print("2. Показать все вакансии")
        print("3. Вывести среднюю зарплату по вакансиям")
        print("4. Показать вакансии с зарплатой выше средней")
        print("5. Найти вакансии по ключевому слову в названии")
        print("6. Выход")

        choice = input("Введите цифру от 1 до 6 для выбора функции работы с вакансиями: ")

        if choice == '1':
            print("\nТоп 10 работодателей по количеству открытых вакансий:")
            for employer in db_manager.get_companies_and_vacancies_count():
                print(f"{employer[0]}. Всего вакансий: {employer[1]}")
        elif choice == '2':
            print("\nСписок всех вакансий:")
            for vacancy in db_manager.get_all_vacancies():
                print(f"Работодатель: {vacancy[0]}. Вакансия: {vacancy[1]} с зарплатой {vacancy[2]}. {vacancy[3]}")
        elif choice == '3':
            print(f"\nСредняя зарплата по всем вакансиям: {round(db_manager.get_avg_salary(), 2)}")
        elif choice == '4':
            print("\nСписок вакансий с зарплатой выше средней:")
            for vacancy in db_manager.get_vacancies_with_higher_salary(db_manager.get_avg_salary()):
                print(f"Работодатель: {vacancy[0]}. Вакансия: {vacancy[1]} с зарплатой {vacancy[2]}. {vacancy[3]}")
        elif choice == '5':
            keyword = input("Введите слово для поиска: ")
            print(f"\nСписок вакансий со словом '{keyword}':")
            for vacancy in db_manager.get_vacancies_with_keyword(keyword):
                print(f"Работодатель: {vacancy[0]}. Вакансия: {vacancy[1]} с зарплатой {vacancy[2]}. {vacancy[3]}")
            db_manager.get_vacancies_with_keyword(keyword)
        elif choice == '6':
            break
        else:
            print("\nВведите цифру от 1 до 6")


if __name__ == '__main__':
    main()