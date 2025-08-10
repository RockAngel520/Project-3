import requests


class HHParser:
    """Класс для работы с сайтом hh.ru через API"""

    def get_employers(self):
        """Метод получения топ 10 работодателей по количеству открытых вакансий"""
        params = {"sort_by": "by_vacancies_open", "per_page": 10}
        response = requests.get("https://api.hh.ru/employers", params=params)
        response.raise_for_status()
        data = response.json()["items"]
        employers = []
        for employer in data:
            employers.append({"id": employer["id"], "name": employer["name"], "open_vacancies": employer["open_vacancies"]})
        return employers

    def get_vacancies_by_employer_id(self, employer_id):
        """Метод получения первых 30 вакансий по id работодателя"""
        params = {"employer_id": employer_id, "per_page": 30}
        response = requests.get("https://api.hh.ru/vacancies", params=params)
        response.raise_for_status()
        data = response.json()["items"]
        vacancies = []
        for vacancy in data:
            salary = vacancy.get("salary")
            if salary:
                salary_from = salary.get("from") or 0
                salary_to = salary.get("to") or 0
                if salary_from and salary_to:
                    salary_avg = (salary_from + salary_to) / 2
                elif salary_from:
                    salary_avg = salary_from
                elif salary_to:
                    salary_avg = salary_to
                else:
                    salary_avg = 0
            else:
                salary_avg = 0

            vacancies.append({
                "id": vacancy["id"],
                "name": vacancy["name"],
                "salary_avg": salary_avg,
                "url": vacancy["alternate_url"],
                "employer_name": vacancy["employer"]["name"],
                "employer_id": vacancy["employer"]["id"],
            })
        return vacancies
