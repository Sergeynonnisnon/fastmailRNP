# coding=UTF-8
import re
import requests
from bs4 import BeautifulSoup
from UA import ua
import sqlite3
import pprint
from db import base

"""
"""


class new_clients():
    def __init__(self):
        pass

    def get_new_clients_href(self, lens=100, number_list=1):
        """
        :param lens: len records on page in url search
        :param number_list: pagination number list
        :return:{serch_query:{number_contract:name,price,date},...}
        """

        result = []
        url = 'https://zakupki.gov.ru/epz/eruz/search/results.html?morphology=on' \
              '&search-filter=Дате+размещения&sortBy=BY_REGISTRY_DATE' \
              f'&pageNumber={number_list}' \
              f'&sortDirection=false&recordsPerPage=_{lens}' \
              '&showLotsInfoHidden=false&participantType_0=on&participantType_1=on' \
              '&participantType_2=on' \
              '&participantType_3=on' \
              '&participantType_4=on' \
              '&participantType_5=on' \
              '&participantType_6=on' \
              '&participantType_7=on' \
              '&participantType=0' \
              '%2C1%2C2%2C3%2C4%2C5%2C6%2C7&registered=on' \
              '&rejectReasonIdNameHidden=%7B%7D' \
              '&countryRegIdHidden=1268%2C' \
              '&countryRegIdNameHidden=%7B"1268"%3A"РОССИЯ"+%7D' \
              '&smallOrMiddle=on'


        response = requests.get(url, headers={'accept': '*/*', 'user-agent': ua.firefox})
        if response.status_code > 200:
            print('requests bad')


        soup = BeautifulSoup(response.text, 'lxml')
        soup = soup.body

        quotes = soup.find_all('div', class_="registry-entry__header-mid__number")

        contract_number = {}
        for i in quotes:
            href = i.find('a')
            href = href.get('href')

            result.append(href)

        return result

    def new_clients_full_info(self, hrefs):
        """
        :param hrefs: list /epz/eruz/card/general-information.html?reestrNumber=21034689
        :return:
        """
        result=[]
        for href in hrefs:
            url = 'https://zakupki.gov.ru'+href
            print(url)
            response = requests.get(url, headers={'accept': '*/*', 'user-agent': ua.firefox})
            if response.status_code > 200:
                print('requests bad')
            soup = BeautifulSoup(response.text, 'lxml')
            soup = soup.body
            quotes = soup.find_all('section', class_="blockInfo__section section")
            for tag in quotes:
                y = tag.find('span',class_='section__title').text
                if y=='Тип участника закупки':
                    type_org = tag.find('span',class_='section__info').text
                if y=='ФИО':
                    FIO = tag.find('span',class_='section__info').text
                if y == 'ИНН':
                    INN = tag.find('span', class_='section__info').text
                if y == 'Адрес электронной почты':
                    email = tag.find('span', class_='section__info').text
                if y == 'Сокращенное наименование':
                    name = tag.find('span', class_='section__info').text

                if y == 'Контактный телефон':
                    phone = tag.find('span', class_='section__info').text

            try:
                name
            except UnboundLocalError:
                name = None
            try:
                FIO
            except UnboundLocalError:
                FIO = None
            try:
                phone
            except UnboundLocalError:
                phone=None
            result.append((name,type_org,FIO,INN,email,phone,0))

            name, type_org, FIO, INN, email, phone = None ,None,None,None,None,None
        return result


    def upgrade_newclients_db(self,info):
        con = sqlite3.connect(f'newclients.db')
        cur = con.cursor()
        for record in info:
            cur.execute(f'''SELECT * FROM newclients WHERE INN=?''', (record [3],))
            check = cur.fetchall()
            if check == []:

                cur.execute(f'INSERT INTO newclients VALUES(?,?,?,?,?,?,?)',record)
                print(record, f'append in newclients ')
            else:
                print(f'alredy in newclients')
        con.commit()
        con.close()

new_clients = new_clients()
base().bd_create(name='newclients', namecol='name text, type_org text, FIO text, INN text, email text, phone text, status email integer')
for i in range(1, 5):
    a=new_clients.get_new_clients_href(lens=100, number_list=i)
    info=new_clients.new_clients_full_info(a)
    new_clients.upgrade_newclients_db(info)

