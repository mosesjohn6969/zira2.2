import time
import random

import openpyxl
import xlwings

#  Loading the workbook
excel_app = xlwings.App(visible=True)
workbookObj = xlwings.Book("algo.xlsx")
MASANIELLO_SHEET = workbookObj.sheets['MASANIELLO']


# excel_book = excel_app.books.open('PATH_TO_YOUR_XLSX_FILE')
#  Creating Object of sheet on which i will be working on


# workbookObj.sheets[MASANIELLO_SHEET].api.Visible = False
# excel_book.save()
# excel_book.close()
# excel_app.quit()
#  Reading CELL Values
# getNextStakeValue = round(MASANIELLO_SHEET['D5'].value)
# print(getNextStakeValue)

#  writing to a file
capital = 50000
total_event = 100
guessed_events = 46
odds = 2

count = 5
currentround = 1

params = [capital, total_event, guessed_events, odds]
for i in params:
    MASANIELLO_SHEET[f"I{count}"].value = i
    count += 1


def gettingAndSettingValues():
    cells = 5
    cellStake = cells
    a = 100
    b = 1
    c = 0

    while True:
        getStakeValue = round(MASANIELLO_SHEET[f'D{cells}'].value)
        getNextStakeValue = getStakeValue
        print(getStakeValue)
        while b < a and getNextStakeValue > 50:
            cellStake += 1
            li = ["W", "L"]
            MASANIELLO_SHEET[f'C{cells}'].value = random.choice(li)
            time.sleep(1)
            getNextStakeValue = round(MASANIELLO_SHEET[f'D{cellStake}'].value)
            print(getNextStakeValue)

            a -= 1
            cells += 1

        a = 100
        b = 1
        cells = 5
        cellStake = cells
        c += 1
        print(f"we got Here {c} times")
        for column in MASANIELLO_SHEET['C5:C104']:
            for cell in column:
                cell.value = None
        time.sleep(2)


gettingAndSettingValues()
