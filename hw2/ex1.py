"""
Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы получаем должность) с сайтов HH(обязательно) и/или Superjob(по желанию). Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:
1. Наименование вакансии.
2. Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
3. Ссылку на саму вакансию.
4. Сайт, откуда собрана вакансия.
"""

from bs4 import BeautifulSoup as bs
import requests
import time
from pprint import pprint
import json
import os.path

result = {
    'name': [],
    'salary': [],
    'vacancy_link': [],
    'website': []
}
url = 'https://hh.ru'
if os.path.isfile('count_html.json'):
    with open('count_html.json', 'r', encoding='utf-8') as f:
        data_for_soup = json.load(f)
else:
    params = {'text': 'python'}
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
        result['name'].append(vacancy_title.text)
        result['vacancy_link'].append(url + vacancy_title['href'])
        vacancy_employer_title = e.find('a', attrs={
            'data-qa': 'vacancy-serp__vacancy-employer'
        })
        if vacancy_employer_title:
            result['website'].append(url + str(vacancy_employer_title["href"]))
        else:
            result['website'].append(None)
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
                result['salary'].append(salary)
            elif salary_text.startswith('от'):
                salary['salary_min'] = int("".join([i for i in salary_text.split() if i.isdigit()]))
                salary['salary_max'] = None
                salary['currency'] = salary_text.split()[-1]
                result['salary'].append(salary)
            else:
                salary['salary_min'] = int("".join([i for i in salary_text.split('–')[0] if i.isdigit()]))
                salary['salary_max'] = int("".join([i for i in salary_text.split('–')[1] if i.isdigit()]))
                salary['currency'] = salary_text.split()[-1]
                result['salary'].append(salary)
        else:
            result['salary'].append(salary)

with open('result.json', 'w', encoding='utf-8') as f:
    json.dump(result, f)

with open('result.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
pprint(data)
