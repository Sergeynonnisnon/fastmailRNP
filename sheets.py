import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_formatting import DataValidationRule, BooleanCondition, set_data_validation_for_cell_range
from typing import Iterable, Dict, List, Set, Tuple
import gspread


validation_rule = DataValidationRule(
    BooleanCondition('BOOLEAN', ['TRUE', 'FALSE']),  # condition'type' and 'values', defaulting to TRUE/FALSE
    showCustomUi=True)


class googlecheets :



def upgrade_googlesheet(insertrow, name_sheet='Макс закупки', worksheet='новая таблица'):
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

    client = gspread.authorize(creds)

    sheet = client.open(f"{name_sheet}").worksheet(worksheet) # Open the spreadhseet

    sheet.append_row([insertrow])

def add_checkbox(cell,name_sheet='Макс закупки'):


    if str(read_googlesheet(cell, name_sheet=name_sheet, worksheet='новая таблица')[0][0]) != 'FALSE':

        scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

        creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

        client = gspread.authorize(creds)

        sheet = client.open(f"{name_sheet}").worksheet('новая таблица')
        set_data_validation_for_cell_range(sheet, cell, validation_rule)
        print(f'{cell} has a checkbox')
    else:
        print(1,type(read_googlesheet(cell, name_sheet=name_sheet, worksheet='новая таблица')[0][0]))

def read_googlesheet(cell, name_sheet='Макс закупки', worksheet='новая таблица'):
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

    client = gspread.authorize(creds)

    sheet = client.open(f"{name_sheet}").worksheet(worksheet)
    answ = sheet.get(cell)
    return answ
add_checkbox('F6')
def upgrade_googlesheet2(cell, name_sheet='Макс закупки', worksheet='новая таблица'):
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

    client = gspread.authorize(creds)

    sheet = client.open(f"{name_sheet}").worksheet(worksheet) # Open the spreadhseet

    set_data_validation_for_cell_range(sheet, cell, validation_rule)
