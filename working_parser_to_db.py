import requests
import pandas as pd
import json
import time
import psycopg2
from psycopg2 import sql

def insert_into_db(vacancy_id, vacancy_name, description, salary_from, salary_to, currency):
    # Параметры подключения к базе данных
    conn = psycopg2.connect(host="localhost",
        port="5433",
        database="data",
        user="postgres",
        password="good")

    # SQL-запрос для вставки данных
    insert_query = '''
        INSERT INTO vacancies (vacancy_id, title, description, salary_from, salary_to, currency)
        VALUES (%s, %s, %s, %s, %s, %s)
    '''

    # Выполнение запроса
    with conn:
        with conn.cursor() as curs:
            curs.execute(insert_query, (vacancy_id, vacancy_name, description, salary_from, salary_to, currency))

    # Закрытие соединения
    conn.close()
    
def parse_vacancies(city_id, vacancy):
    try:
        # Specify the URL for the vacancies API with city and vacancy parameters
        url = 'https://api.hh.ru/vacancies'
        params = {
            'text': vacancy,
            'area': city_id,
            'per_page': 100,
            'search_field': 'name'
        }

        # Send a GET request to the API endpoint
        response = requests.get(url, params=params)


        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            vacancies_data = response.json()

            # Extract and process the relevant information
            for vacancy_info in vacancies_data['items']:
                vacancy_id = vacancy_info['id']
                vacancy_name = vacancy_info['name']
                salary_info = vacancy_info['salary']
                key_skills = vacancy_info.get('key_skills', [])
                key_skills_1 = [skill['name'] for skill in key_skills]
                description = vacancy_info['snippet']['requirement']
                vacancy_salary = vacancy_info.get('salary', {})

                print(f"Vacancy ID: {vacancy_id}")
                print(f"Title: {vacancy_name}")
                print(f"Description: {description}")

                if vacancy_salary:
                    salary_from = vacancy_salary.get('from', 'N/A')
                    salary_to = vacancy_salary.get('to', 'N/A')
                    currency = vacancy_salary.get('currency', 'N/A')
                    print(f"Salary: {salary_from} - {salary_to} {currency}")

                    insert_into_db(vacancy_id, vacancy_name, description, salary_from, salary_to, currency)
                
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            print(f"Response content: {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
city_id = 1  # Moscow city ID (you may need to look up the correct city ID)
vacancy = 'python developer'  # example vacancy

parse_vacancies(city_id, vacancy)