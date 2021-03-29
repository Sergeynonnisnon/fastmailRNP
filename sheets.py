import gspread
from oauth2client.service_account import ServiceAccountCredentials


def upgrade_googlesheet(insertrow, name_sheet='Макс закупки', worksheet='новая таблица'):
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

    client = gspread.authorize(creds)

    sheet = client.open(f"{name_sheet}").worksheet(worksheet) # Open the spreadhseet

    sheet.append_row(insertrow, 2)


