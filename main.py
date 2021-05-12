# coding=UTF-8
from newclients.new_clienst import new_clients

from parse_fast import parse_fastest
from rnp_mail import main as RNP

from db import base
from sheets import googlesheet
import time


def timeit(func):
    def wraper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)

        print('время выполнения ', time.time()-start_time)
        return result
    return wraper
@timeit
def shets():
    for i in range(1, 10):
        parse_fast = parse_fastest()
        parse_fast.get_fast_info([1, ], lens=100, number_list=i)

    bd = base()
    bd.upgrade_child(query='ремонт', name='remont')
    bd.upgrade_sheets('remont')
    print('переходим к удалению старых закупок')
    googlesheet().check_date_ending()
    print('переходим к чекбоксам')
    googlesheet().add_checkbox('F')


@timeit
def main():
    print("начинаем работу с таблицей")
    shets()
    nc = new_clients()

    nc.mailing_newclients()
    print('переходим к наполнению базы данных новыми клиентами')
    start_time = time.time()
    nc.getting()

    print('Время выполнения заполнения базы данных новыми закупками', time.time() - start_time)
    start_time = time.time()
    RNP.main()
    stop_time = time.time()
    print('Время выполнения РНП', stop_time - start_time)


if __name__ == '__main__':
    main()
