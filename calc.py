# -*- coding: utf-8 -*-
"""
Created on Thursday JANUARY 3Oth  13:03:17 2021
@author: MOSES NOKNAN JOHN
Email: mosesjohn12345@gmail.com
phone No: +2348133280825
"""
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# from PyQt5.QtWidgets import QMessageBox
from datetime import date
import datetime
import functools
import os
import time
import sqlite3
import xlwings
import random

# import openpyxl

# import pyttsx3

# python -m PyQt5.uic.pyuic -x log.ui -o log1.py
# pyinstaller ./main.py --onefile --noconsole --add-binary "./driver/chromedriver.exe;./driver"

username = ""
password = ""

flag = 0x08000000


def validation(uname, passWord):  # SETTING DATE VALIDATION FOR SOFTWARE EXECUTION
    today = date.today()
    ExpirationDate = datetime.date(2021, 6, 30)
    username_Input = uname
    password_Input = passWord
    print(username_Input, password_Input)

    if today >= ExpirationDate:
        # textToSpeech = pyttsx3.init()
        print("expired")
        # print(f"YOUR SUBSCRIPTION HAS EXPIRED")
        # voices = textToSpeech.getProperty('voices')  # rendering a voice
        # textToSpeech.setProperty('voice', voices[1].id)  # setting a feminine voice
        # textToSpeech.setProperty('rate', 150)  # setting speed
        # textToSpeech.setProperty('volume', 1)  # setting volume
        # textToSpeech.say(
        #     'YOUR SUBSCRIPTION HAS EXPIRED,  To Renew, CONTACT 08133280825 OR mosesjohn12345@gmail.com.  ' * 3)
        # textToSpeech.runAndWait()
        # msg = QMessageBox()
        # msg.setWindowTitle("Error")
        # msg.setWindowIcon("exit.png")
        # msg.setText("SUBSCRIPTION EXPIRED")
        # msg.setIcon(QMessageBox.Critical)
        # x = msg.exec_()
        return False
    else:
        print("true")
        return True


gecko = os.path.normpath(os.path.join(os.path.dirname(__file__), 'geckodriver'))
print(gecko)


class ZIRA:  # ZIRA CLASS THAT CONTAINS THE BRAIN BOX
    def __init__(self, firstAmount, type):
        self.X = True
        self.pro = 0
        self.won = 0
        self.lost = 0
        self.Time = 0
        self.stake = 0
        self.profit = 0
        self.results = 0
        self.lastStake = 0
        self.PrevAmount = 0
        self.Loosing_STREAK = 0
        self.LostButWinning = 0
        self.currentRound = ""
        self.TextArea = ""
        self.status = ""
        self.result = ""
        self.Type = type
        self.balance = ""
        self.username = ""
        self.password = ""
        self.investment = ""
        self.highestLoosingStreak = 0
        self.logrow = ["", "", "", "", "", "", "", "-₦0", "", "", "", "", ""]

        self.rand = ["HI", "LO"]
        self.Type = random.choice(self.rand)

        #   self.excel_app = xlwings.App(visible=False)
        self.workbookObj = xlwings.Book("algo.xlsx")
        self.MASANIELLO_SHEET = self.workbookObj.sheets['MASANIELLO']

        self.capital = 100000
        self.total_event = 100
        self.guessed_events = 46
        self.odds = 2

        # variables needed in the gettingAndSettingValues method
        self.cells = 5
        self.bal = 5
        self.a = 100
        self.b = 1
        self.c = 0
        self.w = 0
        self.eventsWon = 0
        self.getNextStakeValue = 0
        self.getBalance = 0
        self.gettingAndSettingStatus = "false"

        self.count = 5

        self.params = [self.capital, self.total_event, self.guessed_events, self.odds]
        for i in self.params:
            self.MASANIELLO_SHEET[f"I{self.count}"].value = i
            self.count += 1
        time.sleep(2)
        self.profitByPercent = round(self.MASANIELLO_SHEET[f'I{11}'].value)
        print(self.profitByPercent)

    def gettingStakeAmountAndBalance(
            self):  # getting the value in the D Column (the bet to be made)  gettingStakeAmountAndBalance
        getStakeValue = round(self.MASANIELLO_SHEET[f'D{self.cells}'].value)
        self.getNextStakeValue = getStakeValue

        self.gettingAndSettingStatus = "true"
        return int(self.getNextStakeValue)

    def settingWinOrLoseAndRefreshing(
            self):  # running the logic only if the 100 rounds is still active and the stake value is not less than 50
        if self.b < (self.a - 1) and self.getNextStakeValue > int(
                0.8 * self.capital / 100) and self.getBalance <= self.profitByPercent and self.eventsWon != 46:  # passing in the result of the current round to the spread sheet to facilitate generation of the next stake value

            if self.LastResultType(self.sum_Of_Last_Result()) == "MID":
                self.MASANIELLO_SHEET[f'C{self.cells}'].value = "L"
                time.sleep(1.1)

            elif self.LastResultType(self.sum_Of_Last_Result()) == self.Type:
                self.MASANIELLO_SHEET[f'C{self.cells}'].value = "W"
                time.sleep(1.2)

            elif self.LastResultType(self.sum_Of_Last_Result()) != self.Type:
                self.MASANIELLO_SHEET[f'C{self.cells}'].value = "L"
                time.sleep(1.2)

            self.a -= 1
            self.cells += 1

        else:  # resetting the variables to default values at the end of the 100 round flow
            self.a = 100
            self.b = 1
            self.cells = 5

            self.cells = 5
            self.bal = 5
            self.eventsWon = 0

            self.getBalance = 0
            self.gettingAndSettingStatus = "false"

            self.count = 5  # variable holding the number of times the application has successfully completed a 100 rounds

            rand = ["HI", "LO"]
            self.Type = random.choice(rand)

            for column in self.MASANIELLO_SHEET[
                'C5:C104']:  # clearing the values in all the C cells (win - loss info) so zira can start an new 100 rounds calculation
                for cell in column:
                    cell.value = None
        try:
            self.eventsWon = round(self.MASANIELLO_SHEET[f'I{16}'].value)
            self.getBalance = round(self.MASANIELLO_SHEET[f'F{self.bal}'].value)
            self.bal = self.cells
        except Exception as v:
            print(v, "BUT THIS BUG WAS HANDLED")
            pass

    def LastResultType(self, sumOfBalls):  # DETERMINING WHETHER A ROUND IS EITHER LOW HI OR MID
        self.w = 0
        result = ""
        a = {range(21, 149): "LO", range(149, 152): "MID", range(152, 280): "HI"}
        for key in a:
            if sumOfBalls in key:
                result = a[key]
        return result

    def TimePrecision(self):  # GETTING THE EXACT TIME AND RETURNING THE VALUE NIN INTEGER
        value = 30
        return int(value)

    def sum_Of_Last_Result(self):  # GETTING THE SUM OF TOTAL BALLS RETURNED AND CONVERTING IT TO INTEGER
        # total = input("Sum of Last Round: ")
        time.sleep(1)
        total = random.randint(21, 280)
        self.currentRound = "Current draw: 2469102"

        try:
            self.balance = 100000
        except Exception as g:
            print(g)
            pass
        return int(total)

    def ChoosingBetType(self):
        pass

    def refresh(self):
        try:
            self.ChoosingBetType()
        except Exception as t:
            print(t)
            self.ChoosingBetType()

    def GamePlayAmount(self, Naira):
        pass

    def WinReset(self):
        self.profit += self.LostButWinning
        self.LostButWinning = 0
        self.profit += 50
        self.pro = self.profit
        self.lost = 0
        self.PrevAmount = 0
        self.Loosing_STREAK = 0
        self.status = "WON"
        self.save_to_database()
        print("__" * 28)

    def do_This_When_Loosing(self):
        self.won = 0
        self.LostButWinning += 50
        self.lost += self.stake
        self.Loosing_STREAK += 1
        self.status = "LOST"
        print(f"TOTAL LOST: -₦", self.lost, )

        print("__" * 28)

    def setting_and_placingBets(self):
        self.refresh()
        self.GamePlayAmount(self.stake)
        time.sleep(2)
        self.GamePlayAmount(self.stake)
        time.sleep(3)
        self.placeBet_ExceptionHandling()
        self.PrevAmount = self.stake

    def setting_dont_placingBets(self):
        self.refresh()
        self.GamePlayAmount(self.stake)
        time.sleep(2)
        self.GamePlayAmount(self.stake)
        time.sleep(3)
        self.DontplaceBet_ExceptionHandling()
        self.PrevAmount = self.stake

        print(f"INVESTMENT: ₦{self.stake}")

    def click_on_Last_result_Type(self):

        if self.LastResultType(self.sum_Of_Last_Result()) == "MID":
            if self.Type == "HI":
                pass

            elif self.Type == "LO":
                pass

        elif self.LastResultType(self.sum_Of_Last_Result()) == self.Type:
            if self.Type == "HI":
                pass

            elif self.Type == "LO":
                pass

        elif self.LastResultType(self.sum_Of_Last_Result()) != self.Type:
            if self.Type == "HI":
                pass

            elif self.Type == "LO":
                pass

    def print_and_Log(self):
        print("__" * 28, "\n")
        print(
            f"LAST RESULT {self.sum_Of_Last_Result()}| ROUND:[{self.status}] EVENTS WON:[{self.eventsWon}]|{self.LastResultType(self.sum_Of_Last_Result())}")
        print(
            f"LOST:₦{self.lost} | LOOSING STREAK:[{self.Loosing_STREAK}]| HIGHEST-STREAK: [{self.highestLoosingStreak}] ")
        print(f"INVESTED:₦{self.stake}| MASSANIELLO BALANCE: ₦{self.getBalance}")
        print(f"TOTAL LOST: -₦", self.lost, f" |ACCOUNT BALANCE: ₦{self.balance}")
        print(f"SETTING : ₦{self.stake} FOR NEW ROUND...")

    def save_to_database(self):
        pass

    def savingTodb(self):
        pass

    def waiting(self):
        pass

    def following_the_trend(self):
        if self.LastResultType(self.sum_Of_Last_Result()) == self.Type:
            self.WinReset()

        elif self.LastResultType(self.sum_Of_Last_Result()) != self.Type:
            self.click_on_Last_result_Type()
            self.do_This_When_Loosing()

    def following_the_trend_waiting(self):
        if self.LastResultType(self.sum_Of_Last_Result()) == self.Type:
            pass

        elif self.LastResultType(self.sum_Of_Last_Result()) != self.Type:
            pass

    def sticking_to_one_direction(self):
        if self.LastResultType(self.sum_Of_Last_Result()) == self.Type:
            self.WinReset()

        elif self.LastResultType(self.sum_Of_Last_Result()) != self.Type:
            self.do_This_When_Loosing()

    def placeBet(self):
        pass

    def placeBet_ExceptionHandling(self):
        try:
            self.placeBet()
        except Exception as p:
            print(p)
            self.setting_and_placingBets()

    def DontplaceBet_ExceptionHandling(self):
        pass

    def highest_streak(self):
        if self.Loosing_STREAK >= self.highestLoosingStreak:
            self.highestLoosingStreak = self.Loosing_STREAK

    def BrainBox(self):  # This is the Engine of the bot
        while True:
            if self.sum_Of_Last_Result() != 0:
                print("LOADING...\n")
                while True:
                    while 40 >= self.TimePrecision() >= 20:
                        self.print_and_Log()

                        if self.gettingAndSettingStatus == "true":  # checking if the value has already been gotten from the excel file
                            self.settingWinOrLoseAndRefreshing()  # inputting the last round status into the excel file
                            self.gettingAndSettingStatus = "false"

                        if self.Loosing_STREAK <= 1:
                            if self.sum_Of_Last_Result() != 0:
                                self.stake = self.gettingStakeAmountAndBalance()
                                self.setting_and_placingBets()
                                self.sticking_to_one_direction()
                                self.highest_streak()

                        elif 2 <= self.Loosing_STREAK <= 20:
                            self.waiting()
                            self.setting_dont_placingBets()
                            self.sticking_to_one_direction()
                            self.highest_streak()

                        """  
                        elif 11 <= self.Loosing_STREAK <= 15:
                            self.stake = self.gettingStakeAmountAndBalance()
                            self.setting_and_placingBets()
                            self.sticking_to_one_direction()
                            self.highest_streak()

                        elif 16 <= self.Loosing_STREAK <= 20:
                            self.stake = self.gettingStakeAmountAndBalance()
                            self.setting_and_placingBets()
                            self.sticking_to_one_direction()
                            self.highest_streak()
                        """


def LaunchBot(amount):
    while True:
        try:
            rand = ["HI", "LO"]
            type = random.choice(rand)
            ZIRA(amount, type).BrainBox()
            # x.LaunchDemo()
        except Exception as q:
            print(q)
            pass


if __name__ == '__main__':
    while True:
        try:
            LaunchBot(50)
        except Exception as e:
            print(e)
            pass
