from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke
from bs4 import BeautifulSoup as bs
import requests
import time
from pprint import pprint
import json


def get_vacancy_hh(name: str) -> list:
    """
    name: наименование вакансии
    return: Список вакансий hh.ru
    """
    result = []
    url = 'https://hh.ru'
    params = {'text': name}
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36'}

    response = requests.get(url + '/search/vacancy/', params=params, headers=headers)
    soup = bs(response.text, 'html.parser')
    data = []
    while True:
        data.append(response.text)
        next_link = soup.find('a', attrs={
            'class': "bloko-button",
            'data-qa': "pager-next"
        })
        if next_link:
            time.sleep(1)
            response = requests.get(url + next_link['href'], headers=headers)
            soup = bs(response.text, 'html.parser')
            print(next_link['href'])
        else:
            with open('count_html.json', 'w', encoding='utf-8') as f:
                json.dump({'data': data}, f)
            break
    with open('count_html.json', 'r', encoding='utf-8') as f:
        data_for_soup = json.load(f)
    for el in data_for_soup['data']:
        soup = bs(el, 'html.parser')

        vacancy = soup.find_all('div', attrs={
            'class': 'vacancy-serp-item'
        })
        for e in vacancy:
            vacancy_title = e.find('a', attrs={
                'data-qa': 'vacancy-serp__vacancy-title'
            })
            vacancy_name = vacancy_title.text
            vacancy_link = vacancy_title['href']
            vacancy_employer_title = e.find('a', attrs={
                'data-qa': 'vacancy-serp__vacancy-employer'
            })
            if vacancy_employer_title:
                employer_link = url + str(vacancy_employer_title["href"])
            else:
                employer_link = None
            salary = {
                'salary_min': None,
                'salary_max': None,
                'currency': None
            }
            vacancy_salary = e.find('span', {
                'data-qa': "vacancy-serp__vacancy-compensation"
            })
            if vacancy_salary:
                salary_text = vacancy_salary.getText()
                if salary_text.startswith('до'):
                    salary['salary_max'] = int("".join([i for i in salary_text.split() if i.isdigit()]))
                    salary['salary_min'] = None
                    salary['currency'] = salary_text.split()[-1]
                elif salary_text.startswith('от'):
                    salary['salary_min'] = int("".join([i for i in salary_text.split() if i.isdigit()]))
                    salary['salary_max'] = None
                    salary['currency'] = salary_text.split()[-1]
                else:
                    salary['salary_min'] = int("".join([i for i in salary_text.split('–')[0] if i.isdigit()]))
                    salary['salary_max'] = int("".join([i for i in salary_text.split('–')[1] if i.isdigit()]))
                    salary['currency'] = salary_text.split()[-1]

            result.append({
                'vacancy_name': vacancy_name,
                'vacancy_link': vacancy_link,
                'employer_link': employer_link,
                'salary': salary
            })
    return result


def create_collection_in_databese_mogo(vacancy_name: str, database_name: str = 'vacancy_hh'):
    '''
    vacancy_name: Наименование вакансии,
    database_name: Наименование базы данных (по умолчанию "vacancy_hh").
    '''
    list_vacancy = get_vacancy_hh(vacancy_name)

    client = MongoClient('127.0.0.1', 27017)
    db = client[database_name]

    col = db[vacancy_name]
    try:
        for i, el in enumerate(list_vacancy):
            el['_id'] = i + 1
            col.insert_one(el)
    except dke:
        if (input(f'Хотите обновить коллекцю "{vacancy_name}" введите "*": ')) == '*':
            col.drop()
            for i, el in enumerate(list_vacancy):
                el['_id'] = i + 1
                col.insert_one(el)
        client.close()
    client.close()


vacancy_name = input('Введите вакансию для парсинга: ')
create_collection_in_databese_mogo(vacancy_name)
client = MongoClient('127.0.0.1', 27017)
print(client.list_database_names())
db = client['vacancy_hh']
print(db.list_collection_names())

col = db[vacancy_name]
currency = input('Введите валюту (например: руб., KZT, USD, EUR) = ')
salary = int(input(f'Введите размер заработной платы в {currency} = '))
data = {'data': []}
for doc in col.find({'$or': [
    {'$and': [
        {'$and': [
            {'salary.currency': {'$ne': None}},
            {'salary.currency': {'$eq': currency}},
        ]},
        {'salary.salary_max': {'$ne': None}},
        {'salary.salary_min': {'$ne': None}},
        {'$and': [
            {'salary.salary_min': {'$lte': salary}},
            {'salary.salary_max': {'$gte': salary}},
        ]}
    ]},
    {'$and': [
        {'$and': [
            {'salary.currency': {'$ne': None}},
            {'salary.currency': {'$eq': currency}},
        ]},
        {'salary.salary_max': {'$eq': None}},
        {'salary.salary_min': {'$ne': None}},
        {'salary.salary_min': {'$lte': salary}}
    ]},
    {'$and': [
        {'$and': [
            {'salary.currency': {'$ne': None}},
            {'salary.currency': {'$eq': currency}},
        ]},
        {'salary.salary_max': {'$ne': None}},
        {'salary.salary_min': {'$eq': None}},
        {'salary.salary_max': {'$gte': salary}}
    ]}
]}):
    data['data'].append(doc)
    pprint(doc)
with open(f'Вакансии {vacancy_name} с уровнем дохода {salary} {currency}.json', 'w', encoding='utf-8') as f:
    json.dump(data, f)
