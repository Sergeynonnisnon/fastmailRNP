import re
import requests
from bs4 import BeautifulSoup
from UA import ua

def get_number_contract(list_search, lens=50, number_list=1):
    """

    :param list_search: list to search need to url search zakupki.gov
    :param lens: len records on page in url search
    :param number_list: pagination number list
    :return:{serch_query:{number_contract:name,price,date},...}
    """

    result = {}
    for e in list_search:
        url = 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&fz44=on' \
              '&contractStageList_0=on&contractStageList=0&selectedContractDataChanges=ANY&' \
              'contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=8408974%2C8408975&' \
              f'customerPlaceCodes=%2C&goodsDescription={e}&countryRegIdNameHidden=%7B%7D&' \
              f'sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_{lens}&showLotsInfoHidden=true'

        print(url)
        response = requests.get(url, headers={'accept': '*/*', 'user-agent': ua.firefox})
        if response.status_code > 200:
            print('bad ' + e)
            continue

        soup = BeautifulSoup(response.text, 'lxml')
        soup = soup.body

        quotes = soup.find_all('div', class_="row no-gutters registry-entry__form mr-0")
        contract_number = {}

        for i in quotes:

            href = i.find(class_="registry-entry__header-mid__number")
            href = href.find('a')
            href = href.get('href')

            names = i.find(class_='pl-0 col')
            names = names.text
            names = re.sub(r'\s\s', '', names)
            names = re.sub(r'\n', '', names)

            price = i.find(class_='col d-flex flex-column registry-entry__right-block b-left')
            price = price.find(class_='price-block__value').text
            price = re.sub(r'\s', '', price)
            price = re.sub(r'\n', '', price)

            date = i.find(class_='data-block__value')
            date = date.text
            # проверяем на наличие в таблице
            a = f'zakupki.gov.ru{href}'

            con = sqlite3.connect('rassil.db')
            cur = con.cursor()
            cur.execute('''SELECT contract_number FROM rassil WHERE contract_number = ?''', (a,))

            exists = cur.fetchall()

            if exists == []:
                print(a)
                contract_number[href] = [names, price, date]
                con.commit()
                con.close()

            else:
                print(f"contract alredy in table. {a}")

                con.commit()
                con.close()
                continue

        result[e] = contract_number

    return result
