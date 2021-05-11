# coding=UTF-8
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_formatting import DataValidationRule, BooleanCondition, set_data_validation_for_cell_range

import gspread
import time
from datetime import datetime


class googlesheet:
    def __init__(self, name_sheet='Макс закупки', worksheet='новая таблица'):

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

    def upgrade_googlesheet(self, insertrow):
        """
        insert row in last empty row in google sheet
        :param insertrow: apending list
        :return: None
        """
        self.sheet.append_row(insertrow)

    def read_googlesheet(self, cell):
        """
        Reead data in cell
        :param cell: str ,cell in googlesheets
        :return: str
        """
        return self.sheet.get(cell)

    def add_checkbox(self, cell='F'):
        """
        add checkbox in cell
        :param cell: cell in googlesheets
        :return: None
        """
        _col_f = self.sheet.col_values(6)
        set_data_validation_for_cell_range(self.sheet, cell, self.validation_rule)



    def check_date_ending(self):
        """
        check if filing date  is finish
        :return: None
        """
        now = datetime.now()

        col_e = self.sheet.col_values(5)[1:]
        col_f = self.sheet.col_values(6)[1:]

        y = 0
        del_row = []

        for i in col_e:

            deadline = datetime.strptime(i, "%d.%m.%Y")
            try:
                if now > deadline and col_f[y] != 'TRUE':
                    del_row.append(y + 2)
            except IndexError:
                pass
            finally:
                y += 1
        for i in reversed(del_row):
            self.sheet.delete_rows(i)
            print(f'Удалена запись № {i} т.к. окончание подачи заявок прошло')


