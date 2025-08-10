import psycopg2
from config import config
from src.hh_parser import HHParser

def create_database(db_name):
    """Функция создания базы данных с заданным именем"""
    params = config()
    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
    cur.execute(f"CREATE DATABASE {db_name}")

    cur.close()
    conn.close()


def create_tables(db_name):
    """Функция создания таблиц employers и vacancies"""
    params = config()
    with psycopg2.connect(dbname=db_name, **params) as conn:
        with conn.cursor() as cur:
            cur.execute("CREATE TABLE employers ("
                        "id INT PRIMARY KEY,"
                        "name VARCHAR(255) NOT NULL,"
                        "open_vacancies INT)")

        with conn.cursor() as cur:
            cur.execute("CREATE TABLE vacancies ("
                        "vacancy_id INT PRIMARY KEY,"
                        "vacancy_name VARCHAR(255) NOT NULL,"
                        "salary FLOAT,"
                        "url VARCHAR(255) NOT NULL,"
                        "employer_name VARCHAR(255) NOT NULL,"
                        "employer_id INT REFERENCES employers(id))")

    conn.close()


def insert_employers(db_name):
    """Функция заполнения таблицы employers данными с сайта hh.ru"""
    hh_parser = HHParser()
    employers = hh_parser.get_employers()
    params = config()
    with psycopg2.connect(dbname=db_name, **params) as conn:
        with conn.cursor() as cur:
            for employer in employers:
                cur.execute("INSERT INTO employers VALUES (%s, %s, %s)", (employer["id"], employer["name"], employer["open_vacancies"]))
    conn.close()


def get_employers_id():
    """Функция получения списка id топ работодателей"""
    hh_parser = HHParser()
    employers = hh_parser.get_employers()
    employers_id = []
    for employer in employers:
        employers_id.append(employer["id"])

    return employers_id


def insert_vacancies(db_name):
    """Функция заполнения таблицы vacancies данными с сайта hh.ru"""
    hh_parser = HHParser()
    employers_id = get_employers_id()
    vacancies = []
    for employer_id in employers_id:
        vacancies_by_employer_id = hh_parser.get_vacancies_by_employer_id(employer_id)
        for vacancy in vacancies_by_employer_id:
            vacancies.append(vacancy)
    params = config()
    with psycopg2.connect(dbname=db_name, **params) as conn:
        with conn.cursor() as cur:
            for vacancy in vacancies:
                cur.execute("INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s)", (vacancy["id"], vacancy["name"],
                        vacancy["salary_avg"], vacancy["url"], vacancy["employer_name"], vacancy["employer_id"]))
    conn.close()
