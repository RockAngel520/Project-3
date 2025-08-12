import psycopg2

from config import config


class DBManager:
    """Класс для работы с БД PostgreSQL"""

    def __init__(self, db_name: str):
        """Метод инициализации класса DBManager"""
        self.__db_name = db_name

    def __execute_query(self, query: str):
        """Метод для выполнения запросов к БД"""
        params = config()
        with psycopg2.connect(dbname=self.__db_name, **params) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
        conn.close()
        return result

    def get_companies_and_vacancies_count(self):
        """Метод, который получает список всех компаний и количество вакансий у каждой компании"""
        query = (
            "select employers.name, vacancy_name, salary, url FROM vacancies INNER JOIN employers ON "
            "vacancies.employer_id=employers.id"
        )
        return self.__execute_query(query)

    def get_all_vacancies(self):
        """Метод, который получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты
        и ссылки на вакансию"""
        query = (
            "select employers.name, vacancy_name, salary, url FROM vacancies INNER JOIN employers ON "
            "vacancies.employer_id=employers.id"
        )
        return self.__execute_query(query)

    def get_avg_salary(self) -> float:
        """Метод, который получает среднюю зарплату по вакансиям"""
        query = "SELECT AVG(salary) FROM vacancies"
        return self.__execute_query(query)[0][0]

    def get_vacancies_with_higher_salary(self, avg_salary: float):
        """Метод, который получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        query = (
            f"select employers.name, vacancy_name, salary, url FROM vacancies INNER JOIN employers ON "
            f"vacancies.employer_id=employers.id WHERE salary > {avg_salary} ORDER BY salary DESC"
        )
        return self.__execute_query(query)

    def get_vacancies_with_keyword(self, keyword: str):
        """Метод, который получает список всех вакансий с переданным словом"""
        query = (
            f"select employers.name, vacancy_name, salary, url FROM vacancies INNER JOIN employers ON "
            f"vacancies.employer_id=employers.id WHERE LOWER(vacancy_name) LIKE '%{keyword.lower()}%'"
        )
        return self.__execute_query(query)
