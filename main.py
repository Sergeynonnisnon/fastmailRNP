# coding=UTF-8
from newclients.new_clienst import new_clients
from newclients.mailing import newclients_mailing
from parse_fast import parse_fastest

import logging

from db import base
from sheets import googlesheet
import sys,time, os


def shets():
    for i in range(1,10):
        parse_fast = parse_fastest()
        fast_info = parse_fast.get_fast_info([1, ], lens=100, number_list=i)

    bd = base()
    bd.upgrade_child(query='ремонт', name='remont')
    bd.upgrade_sheets('remont')
    time.sleep(60)
    googlesheet().add_checkbox('F')
    time.sleep(60)

    googlesheet().check_date_ending()



def get_logger():
    logger = logging.getLogger("threading_example")
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler("threading.log")
    fmt = '%(asctime)s - %(threadName)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)

    logger.addHandler(fh)
    return logger


def main():

    start_time = time.time()
    shets()
    stop_time = time.time()

    print('Время выполнения заполнения гугл таблиц', stop_time-start_time)
    start_time = time.time()
    nc = new_clients()

    #nc.mailing_newclients()
    stop_time = time.time()
    print('Время выполнения  отправления писем', stop_time - start_time)
    start_time = time.time()
    nc.getting()
    stop_time = time.time()
    print('Время выполнения заполнения базы данных новыми закупками', stop_time - start_time)

if __name__ == '__main__':
    main()
