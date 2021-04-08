# coding=UTF-8
import sys
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sqlite3

from sheets import upgrade_googlesheet


def bd_create(name='oll',namecol=None):

    con = sqlite3.connect(f'{name}.db')
    cur = con.cursor()

    cur.execute(f'''CREATE TABLE  {name} ({namecol})''')

    con.commit()
    con.close()



def upgrade_child(query,name):
    con = sqlite3.connect(f'oll.db')
    cur = con.cursor()
    cur.execute('''SELECT name_trade FROM oll ''')
    exists = cur.fetchall()
    info=[]
    for name_trade in exists:

        if name_trade[0].find(query) >= 0:
            cur.execute(f'''SELECT * FROM oll WHERE name_trade=?''',name_trade)
            need_info = cur.fetchall()

            if len(need_info)>0:
                info.append(need_info)
            need_info = []
    con.commit()
    con.close()
    con = sqlite3.connect(f'{name}.db')
    cur = con.cursor()
    if len(info)>0:
        for i in info:
            cur.execute(f'''SELECT * FROM {name} WHERE con_num=?''', (i[0][0],))
            in_query = cur.fetchall()

            if in_query == []:

                cur.execute(f'INSERT INTO {name} VALUES(?,?,?,?,?,?)',
                        i[0])
                print(i[0][0],f'append in {name} ')
            else:
                print(f'alredy in {name}')
    con.commit()
    con.close()
def upgrade_sheets(name_table, name_sheet='Макс закупки', worksheet='новая таблица'):
    con = sqlite3.connect(f'{name_table}.db')
    cur = con.cursor()
    cur.execute(f'''SELECT * FROM {name_table} WHERE on_sheets=0''')
    exists = cur.fetchall()
    if  exists!=[]:
        for i in exists:
            print(i[0])
            upgrade_googlesheet(i[:-1],name_sheet='Макс закупки', worksheet='новая таблица')
            cur.execute(f'''UPDATE  {name_table} set on_sheets=1 WHERE con_num=?''',(i[0],))

    con.commit()
    con.close()



#bd_create(name="oll",namecol='con_num text,name_trade text,price text, date text,deadline text,on_sheets text')