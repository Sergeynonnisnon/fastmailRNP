# coding=UTF-8

from parse_fast import parse_fastest
from parse_full import *

from db import base
from sheets import googlesheet
import sys, time, os





def main():
    start_time = time.time()

    for i in range(1,1):
        parse_fast = parse_fastest()
        fast_info = parse_fast.get_fast_info([1, ], lens=50, number_list=i)

    bd = base()
    bd.upgrade_child(query='ремонт', name='remont')
    bd.upgrade_sheets('remont')
    googlesheet().add_checkbox('F')
    googlesheet().check_date_ending()

    stop_time = time.time()


if __name__ == '__main__':
    main()
