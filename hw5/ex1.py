"""
Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
Логин тестового ящика: some_name
Пароль тестового ящика: some_password
"""




import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import hashlib
import pprint
import json
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke
from selenium.common.exceptions import NoSuchElementException as nsee

from selenium.webdriver.common.action_chains import ActionChains
import pprint
import time


def create_collection_in_databese_mogo(collection_name: str, news_list: list, database_name: str = 'my_mongoDB'):
    '''
    collection_name: Наименование коллекции;
    news_list: контент;
    database_name: Наименование базы данных (по умолчанию "my_mongoDB").
    '''

    client = MongoClient('127.0.0.1', 27017)
    db = client[database_name]

    col = db[collection_name]

    for i, el in enumerate(news_list):
        try:
            col.insert_one(el)
        except dke:
            print('Есть такой контент!')

    client.close()


def selenium_demo():
    options = Options()
    options.add_argument("start-maximized")

    s = Service('./chromedriver')
    driver = webdriver.Chrome(service=s, options=options)

    driver.get('https://mail.ru/')

    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH,
         '//button[@class="resplash-btn resplash-btn_primary resplash-btn_mailbox-big svelte-160g8vb"]'))).click()
    driver.implicitly_wait(10)

    driver.switch_to.frame(driver.find_element(By.XPATH, '//iframe[@class="ag-popup__frame__layout__iframe"]'))

    driver.find_element(By.NAME, "username").send_keys("some_name")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, '//button[@class="base-0-2-79 primary-0-2-93"]'))).click()

    driver.find_element(By.NAME, "password").send_keys("some_password")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, '//button[@class="base-0-2-79 primary-0-2-93"]'))).click()

    list_link_message = []
    flag = True
    while True:
        try:
            if flag:
                time.sleep(.5)
                first_element = driver.find_element(By.XPATH, "//a[contains(@class,'llc llc_normal llc_first')]")
                driver.implicitly_wait(1)
            last_element = driver.find_element(By.XPATH, "//a[contains(@class,'llc llc_normal llc_last')]")
            links = WebDriverWait(driver, 10).until(lambda x: x.find_elements(By.XPATH,
                                                                              "//a[contains(@class,'llc llc_normal llc_new')]"))
            links.append(last_element)
            if flag:
                links.append(first_element)
            links_str = [el.get_attribute("href") for el in links]
            list_link_message = list_link_message + links_str
            break
        except nsee:
            links = WebDriverWait(driver, 10).until(lambda x: x.find_elements(By.XPATH,
                                                                              "//a[contains(@class,'llc llc_normal llc_new')]"))
            if flag:
                links.append(first_element)
                flag = False
            links_str = [el.get_attribute("href") for el in links]
            list_link_message += links_str
            ActionChains(driver).move_to_element(links[-1]).perform()

    list_link_message = list(set(list_link_message))
    flag = True
    for link in list_link_message:
        temp = {
            '_id': hashlib.sha256(bytes(link, encoding='utf8')).hexdigest(),
            'date': str(datetime.datetime.now())
        }
        if flag:
            driver.switch_to.new_window('window')
            flag = False
        driver.get(link)

        driver.implicitly_wait(10)
        # //div[@class="letter__header-details"]
        time.sleep(.5)
        temp['message_date'] = driver.find_element(By.XPATH, '//div[@class="letter__date"]').text
        print(temp['message_date'])
        temp['message_from'] = driver.find_element(By.XPATH, '//div[@class="letter__author"]/span').get_attribute(
            'title')
        print(temp['message_from'])
        temp['message_subject'] = driver.find_element(By.XPATH, '//h2[@class="thread-subject"]').text
        print(temp['message_subject'])
        print('_______________________________________________________')
        temp['message_text'] = driver.find_element(By.XPATH, "//*[contains(@id, '_BODY')]").text
        print(temp['message_text'])
        create_collection_in_databese_mogo('Mail_message', [temp])

if __name__ == '__main__':
    #selenium_demo()

    client = MongoClient('127.0.0.1', 27017)
    db = client['my_mongoDB']
    #db.drop_collection('Mail_message')
    col = db['Mail_message']
    data = {'data': list(col.find({}))}
    with open("data_from_mongo.json", "w", encoding='utf-8') as f:
        json.dump(data, f)

    # options = Options()
    # options.add_argument("start-maximized")
    #
    # s = Service('./chromedriver')
    # driver = webdriver.Chrome(service=s, options=options)
    #
    # driver.get('https://mail.ru/')
    #
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    #     (By.XPATH,
    #      '//button[@class="resplash-btn resplash-btn_primary resplash-btn_mailbox-big svelte-160g8vb"]'))).click()
    # driver.implicitly_wait(10)
    #
    # driver.switch_to.frame(driver.find_element(By.XPATH, '//iframe[@class="ag-popup__frame__layout__iframe"]'))
    #
    # driver.find_element(By.NAME, "username").send_keys("study.ai_172@mail.ru")
    #
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    #     (By.XPATH, '//button[@class="base-0-2-79 primary-0-2-93"]'))).click()
    #
    # driver.find_element(By.NAME, "password").send_keys("NextPassword172#")
    #
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    #     (By.XPATH, '//button[@class="base-0-2-79 primary-0-2-93"]'))).click()
    # driver.implicitly_wait(10)
    # time.sleep(3)
    # first_element = driver.find_element(By.XPATH, "//a[contains(@class,'llc llc_normal llc_first')]")
    #
    # driver.get(first_element.get_attribute('href'))
    #
    # date = datetime.datetime
    # date = str(datetime.datetime.now())
    #
    # message_date = driver.find_element(By.XPATH, '//div[@class="letter__date"]').text
    # print(message_date)
    # message_from = driver.find_element(By.XPATH, '//div[@class="letter__author"]/span').get_attribute('title')
    # print(message_from)
    # message_subject = driver.find_element(By.XPATH, '//h2[@class="thread-subject"]').text
    # print(message_subject)
    # print('_______________________________________________________')
    # message_text = driver.find_element(By.XPATH, "//*[contains(@id, '_BODY')]").text
    # print(message_text)
