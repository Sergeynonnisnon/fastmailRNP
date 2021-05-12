import re
import time
import sys
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


from rnp_mail.mail import *

ua = UserAgent()




def get_href(lens,number_list):
    """

    :return: lits 'decision_number'
    """
    print(f"вы выбрали спарсить страницу № {number_list} , дождитесь окончания работы скрипта")
    url = 'https://zakupki.gov.ru/epz/dizk/search/results.html?searchString=&morphology=on&search-filter=Дате+размещения' \
          f'&pageNumber={number_list}&sortDirection=false&recordsPerPage=_{lens}&showLotsInfoHidden=false&savedSearchSettingsIdHidden=' \
          '&sortBy=UPDATE_DATE&published=on&ur=on&fg=on&fs=on&customerIdOrg=&customerFz94id=&customerTitle=&agencyIdOrg=' \
          '&customerFz94id=&customerTitle=&customerPlace=&customerPlaceCodes=&registerContractNumber=&contractNumber=&order' \
          'Number=&orderName=&placingWayList=&selectedLaws=&supplier=&inn=&kpp=&contractDateFrom=&contractDateTo=&publishDateFrom' \
          '=&publishDateTo=&updateDateFrom=&updateDateTo=&searchTextInAttachedFile='

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find_all('div', class_='registry-entry__header-mid__number')
    result = []
    for elem in quotes:
        m = re.search(r'\d{6}', str(elem))
        result.append(m.group())

    return result


def number_contract(numbers):
    """

    :param numbers: list of 'decision_number'
    :return: dict {'decision_number' :'contract_number'}
    """
    answers = {}
    for i in numbers:

        url = f'https://zakupki.gov.ru/epz/dizk/dizkCard/generalInformation.html?dizkId={i}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find_all('span', class_='section__info', limit=4)
        for elem in quotes:
            m = re.search(r'\d{19}', str(elem))
            try:

                answers[i] = m.group()
            except:
                answers[i] = None

    print(answers)
    return answers


def response(answers):
    for i in answers:
        urls = 'https://zakupki.gov.ru/epz/contract/contractCard/common-info.html?reestrNumber='
        url = urls + str(answers[i])
        if url is not None:
            response = requests.get(url, headers={'accept': '*/*', 'user-agent': ua.firefox})
        else:
            continue

        if response.status_code == 404:
            time.sleep(2)
            print('404')


def get_email(answers):
    """
    :param answers: gives dict numbers contacts like { '147046': '2272291208821000036'}}
    :return: dict {'decision_number': 'contract_number ','email',...}
    """
    a = 0
    for i in answers:
        a += 1
        urls = 'https://zakupki.gov.ru/epz/contract/contractCard/common-info.html?reestrNumber='
        url = urls + str(answers[i])
        time.sleep(1)
        if url is not None:
            response = requests.get(url, headers={'accept': '*/*', 'user-agent': ua.firefox})

        else:

            continue

        if response.status_code == 404:
            time.sleep(2)
            print('ошибка 404')
        print(f'загружено {a} ссылок')
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find_all('div', class_='container')

        try:
            m = re.search(r'[\w+\.-]*\w+@[\w+\.]*\w+[\w+\-\w+]*\.\w+', str(quotes))
            answers[i] = [answers[i], m.group()]
        except:
            answers[i] = [answers[i], None]
            continue
    return answers


def bd_create():
    """create db on base path
    :return: bd RNP with colums where :
    decision_number - number in link of desision to send RNP
    contract_number- contract number in link
    email -email in scrap contract,
    status - 1/0 1- no send email 0 - email send
    email_status- 1- email exist 0- email dont exist"""
    con = sqlite3.connect('RNP.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE RNP
                   (decision_number text,  contract_number text, email text, 
                    status real,email_status)''')
    con.commit()
    con.close()


def upgrade_row(answers):
    """
    upgrade the db with rule - if desision_number in db= dont append row,
    else - append db answers and check have row a email
    :param answers: dict like 'decision_number': 'contract_number ','email'
    :return: None
    """
    con = sqlite3.connect('RNP.db')
    cur = con.cursor()

    for i in answers:

        if answers[i][1] is not None:
            add = [i, answers[i][0], answers[i][1], 1, 1]
        else:
            add = [i, answers[i][0], answers[i][1], 1, 0]

        cur.execute(f'''SELECT decision_number FROM RNP WHERE decision_number={i}''')
        exists = cur.fetchall()
        if not exists:
            cur.execute('INSERT INTO RNP VALUES(?,?,?,?,?)', add)
            con.commit()
        else:
            print(f"url alredy in table.{add}")

            continue

    con.commit()
    con.close()


def main():
    number_list = 1
    lens = 100
    href = get_href(lens, number_list)
    number = number_contract(href)
    email = get_email(number)
    upgrade_row(email)
    mailing()
