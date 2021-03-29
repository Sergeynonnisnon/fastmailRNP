# coding=UTF-8
import sys
import time
import sqlite3
from sheets import *
def bd_create(name='rassil',namecol=None):

    con = sqlite3.connect(f'{name}.db')
    cur = con.cursor()
    cur.execute(f'''CREATE TABLE {name} 
                               ( {namecol})''')
    con.commit()
    con.close()


def upgrade_row(contract_number, sheet):
    """
    upgrade the db with rule - if desision_number in db= dont append row,
    else - append db answers and check have row a email
    :param contract_number: dict search_query text,  contract_number text, name text, inn text,tel_email text,
                                status real
    :param sheet : number sheet in google sheet
    :return: None
    """
    con = sqlite3.connect('rassil.db')
    cur = con.cursor()

    for i in contract_number:
        con_num = None
        name_trade = None
        price = None
        date = None
        org_name = None
        inn = None
        tel_email = None
        search_query = i
        for e in contract_number[i]:

            con_num = f'zakupki.gov.ru{e}'
            name_trade = contract_number[i][e][0]
            price = contract_number[i][e][1]
            date = contract_number[i][e][2]
            org_name = contract_number[i][e][3][0]
            inn = contract_number[i][e][3][1]
            tel_email = contract_number[i][e][3][2]

            try:
                cur.execute('''SELECT contract_number FROM rassil WHERE contract_number = ?''', (con_num,))

            except(sqlite3.OperationalError):
                pass

            exists = cur.fetchall()

            if exists == []:
                cur.execute('INSERT INTO rassil VALUES(?,?,?,?,?,?,?,?,?)',
                            (search_query, con_num, name_trade, price, date, org_name, inn, tel_email, 0))
                con.commit()
                if sheet == 1:
                    upgrade_googlesheet([search_query, con_num, name_trade, price, date, org_name, inn, tel_email])
                    print(f'Добавлено {search_query, con_num} в таблицу')
                if sheet == 2:
                    upgrade_googlesheet2([search_query, con_num, name_trade, price, date, org_name, inn, tel_email])
                    print(f'Добавлено {search_query, con_num} в таблицу')
            else:
                print(f"contract alredy in table. {con_num}")
                continue
    con.commit()
    con.close()