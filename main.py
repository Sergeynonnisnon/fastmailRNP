# полная база закупок с автообновлением раз в 4 часа
# coding=UTF-8


from parse_fast import *
from parse_full import *
from db import *
from sheets import upgrade_googlesheet




def main():
    #for i in range(20):
    #    fast_info = get_fast_info([1, ], lens=50, number_list=i)
    #upgrade_child(query='ремонт', name='remont')
    upgrade_sheets('remont')
    #time.sleep(10)
    #sys.exit()



if __name__ == '__main__':
    main()
