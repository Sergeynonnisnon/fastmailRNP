import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_formatting import DataValidationRule, BooleanCondition, set_data_validation_for_cell_range
from typing import Iterable, Dict, List, Set, Tuple
import gspread
import time
from datetime import datetime





class googlesheet():
    def __init__(self,name_sheet='Макс закупки',worksheet='новая таблица'):

        self.name_sheet = name_sheet
        self.worksheet = worksheet
        self.validation_rule = DataValidationRule(BooleanCondition('BOOLEAN', ['TRUE', 'FALSE']),
                                                  # condition'type' and 'values', defaulting to TRUE/FALSE
            showCustomUi=True)
        self.scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        self.creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", self.scope)
        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open(f"{name_sheet}").worksheet(worksheet)
        self.col_values=self.sheet.col_values(1)

    def upgrade_googlesheet(self,insertrow):
        """
        insert row in last empty row in google sheet
        :param insertrow: list
        :return: None
        """
        self.sheet.append_row([insertrow])


    def read_googlesheet(self,cell):
        """
        Reead data in cell
        :param cell: str ,cell in googlesheets
        :return: str
        """
        return self.sheet.get(cell)

    def add_checkbox(self,cell):
        """
        add checkbox in cell
        :param cell: cell in googlesheets
        :return: None
        """
        set_data_validation_for_cell_range(self.sheet, cell, self.validation_rule)

    def check_checkbox_exist(self):
        """
        add checkbox in F col if not exist
        :return:
        """
        #print(len(self.sheet.col_values(1)))
        for i in range(2,len(self.col_values)+1):
            try:
                if str(self.read_googlesheet(f'F{i}')) == '[]':
                    print(f'F{i} add', self.read_googlesheet(f'F{i}'))
                    self.add_checkbox(f'F{i}')

                #print(self.read_googlesheet(f'F{i}'))
            except(gspread.exceptions.APIError):
                print()
                time.sleep(60)
    def check_date_ending (self):
        now =datetime.now().strftime("%d.%m.%Y")

        for i in range(2, len(self.col_values)-2 ):
            print(str(self.read_googlesheet(f'E{i}')))
            try:

                if now>str(self.read_googlesheet(f'E{i}')[0][0]) and\
                    str(self.read_googlesheet(f'F{i}')) !=str([['TRUE']]) :
                    print(str(self.read_googlesheet(f'F{i}')))
                    print(now,str(self.read_googlesheet(f'E{i}')))

                    self.sheet.delete_rows(i,i)


            except(gspread.exceptions.APIError,IndexError):
                if Exception(IndexError):
                    print('1')
                    pass

                print(1)
                time.sleep(60)








googlesheet=googlesheet()
googlesheet.check_date_ending()

"""

    def add_checkbox(cell):
        if str(self.read_googlesheet(cell, name_sheet=name_sheet, self.worksheet) != 'FALSE':

            set_data_validation_for_cell_range(self.sheet, cell, self.validation_rule)
            print(f'{cell} has a checkbox')
        else:
            print(1, type(read_googlesheet(cell, name_sheet=name_sheet, worksheet='новая таблица')[0][0]))

    def read_googlesheet(cell, name_sheet='Макс закупки', worksheet='новая таблица'):
        scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

        creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

        client = gspread.authorize(creds)

        sheet = client.open(f"{name_sheet}").worksheet(worksheet)
        answ = sheet.get(cell)
        return answ



    def upgrade_googlesheet2(cell, name_sheet='Макс закупки', worksheet='новая таблица'):
        scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

        creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

        client = gspread.authorize(creds)

        sheet = client.open(f"{name_sheet}").worksheet(worksheet)  # Open the spreadhseet

        set_data_validation_for_cell_range(sheet, cell, self.validation_rule)


"""



