import re
import requests
from bs4 import BeautifulSoup
def get_contract_info(fast_contract_info):
    """

    :param fast_contract_info:  {serch_query:{number_contract:name,price,date},...}
    :return: {serch_query:{number_contract:name,price,date,name,inn,telemail},...}
    """

    for contract_number in fast_contract_info:

        contract_info = []
        for i in fast_contract_info[contract_number]:

            info = []
            url = f'https://zakupki.gov.ru{i}'
            response = requests.get(url, headers={'accept': '*/*', 'user-agent': ua.firefox})
            if response.status_code > 200:
                print('bad ' + i)
                continue
            soup = BeautifulSoup(response.text, "lxml")

            table = soup.select('tbody', class_="tableBlock__row")[-1]
            table = table.find_all('td')

            for e in table:
                if str(e.text).find('Об ограничениях допуска отдельных видов промыш') == -1 and \
                        str(e.text).find('Участникам, заявки или окончательные предложения которых содержат') == -1 \
                        and str(e.text).find('допуска') == -1 \
                        and str(e.text).find('руб'):
                    e = re.sub(r'\s\s', '', e.text)
                    e = e.split('\n')

                    info.append(e)
            info = parse_string(info)

            contract_info.append(info)

            contract_info = fast_contract_info[contract_number][i] + contract_info
            fast_contract_info[contract_number][i] = contract_info
            contract_info = []

    return fast_contract_info



def parse_string(string):
    name = None
    inn = None
    tel_email = None

    for i in string:
        if type(i) == list:

            for list_element in i:
                if list_element.find('ООО') >= 1 or list_element.find('ИНДИВИДУАЛЬНЫЙ') >= 1 \
                        or list_element.find('Индивидуальный') >= 1 \
                        or list_element.find('Общество') >= 1 \
                        or list_element.find('ОБЩЕСТВО') >= 1 \
                        or list_element.find('Учреждение') >= 1 \
                        or list_element.find('УЧРЕЖДЕНИЕ') >= 1:
                    name = list_element

                if list_element.find('ИНН:') >= 0:
                    inn = i[i.index(list_element) + 1]
                if list_element.find('@') >= 0:
                    tel_email = list_element
        if type(i) == str:
            if i.find('ООО') >= 0 or i.find('ИНДИВИДУАЛЬНЫЙ') >= 0:
                name = i

            if i.find('ИНН:') >= 0:
                inn = string[string.index(i) + 1]
            if i.find('@') >= 0:
                tel_email = i

    print('получаю данные по контактам внутри контракта _____')
    return name, inn, tel_email