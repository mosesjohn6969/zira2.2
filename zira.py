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
from datetime import date, datetime
import datetime
import functools
import os
import time
import sqlite3
import xlwings
import random

# import openpyxl

# import pyttsx3

t = time.localtime()

# python -m PyQt5.uic.pyuic -x log.ui -o log1.py
# pyinstaller ./main.py --onefile --noconsole --add-binary "./driver/chromedriver.exe;./driver"

username = ""
password = ""

flag = 0x08000000


def validation(uname, passWord):  # SETTING DATE VALIDATION FOR SOFTWARE EXECUTION
    today = date.today()
    ExpirationDate = datetime.date(2021, 12, 30)
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
        webdriver.common.service.subprocess.Popen = functools.partial(webdriver.common.service.subprocess.Popen,
                                                                      creationflags=flag)
        self.driver = webdriver.Firefox(executable_path=gecko + ".exe")
        self.driver.maximize_window()
        self.X = True
        self.pro = 0
        self.won = 0
        self.lost = 0
        self.Time = 0
        self.stake = 0
        self.profit = 0
        self.lastStake = 0
        self.PrevAmount = 0
        self.Loosing_STREAK = 0
        self.LostButWinning = 0
        self.currentRound = ""
        self.TextArea = ""
        self.status = ""
        self.balance = ""
        self.result = ""
        self.Type = type
        self.username = ""
        self.password = ""
        self.investment = ""
        self.highestLoosingStreak = 0
        self.InitialAmount = firstAmount
        self.logrow = ["", "", "", "", "", "", "", "-₦0", "", "", "", "", ""]
        self.winHandleBefore = self.driver.window_handles[0]

        self.timepre = 0
        self.cell = 4
        self.a = 1
        self.workbookObj = xlwings.Book("algoh.xlsx")
        self.MASANIELLO_SHEET = self.workbookObj.sheets['MASANIELLO']

    def closeAds(self):
        try:
            time.sleep(3)
            self.driver.find_element_by_xpath("/html/body/div[2]/section/main/div/div[1]/button").click()
        except Exception as e:
            pass

    def login(self):  # THIS TAKES US THROUGH THE LOGIN PROCESS TO THE GAME PLAY
        self.driver.get('https://mobile.bet9ja.com/Mobile')

        login_btn = self.driver.find_element_by_xpath('//*[@id="header_link_login"]/i')  # CLICKING THE LOGIN BUTTON
        login_btn.click()
        # SETTING USERNAME AND PASSWORD

        self.closeAds()
        TextAreaU = self.driver.find_element_by_xpath('//*[@id="wrapper"]/main/div/div/div/div[2]/div/input')
        time.sleep(2)
        TextAreaU.send_keys(Keys.CONTROL, 'a')
        time.sleep(2)
        TextAreaU.send_keys(self.username)

        TextAreaP = self.driver.find_element_by_xpath('//*[@id="wrapper"]/main/div/div/div/div[3]/div/input')
        time.sleep(2)
        TextAreaP.send_keys(Keys.CONTROL, 'a')
        time.sleep(2)
        TextAreaP.send_keys(self.password)
        self.driver.find_element_by_xpath('//*[@id="wrapper"]/main/div/div/div/button').click()
        self.closeAds()

        try:  # CLOSING ANY POP UP UPON LOGIN
            time.sleep(4)
            self.driver.find_element_by_xpath("//a[contains(text(), 'x')]").click()

        except Exception as s:
            print(s)
            pass

        try:
            s = self.driver.find_element_by_class_name("info").text
            print(s)
        except Exception as j:
            print(j)
            self.closeAds()
            self.driver.get("https://casino.bet9ja.com/casino/category/all")
            time.sleep(7)
            self.closeAds()
            try:  # LOCATING BET49
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="11000"]/div/div[1]/img')))
            except WebDriverException as a:
                print(a)

            self.driver.execute_script('window.scrollTo(0,40)')  # SCROLLING DOWN TO THE POINT
            imgPath = "/html/body/div[1]/div/div/main/div[1]/div[2]/div[2]/div/div[3]/div[2]/div[4]/div[3]/div/div[1]/img"
            self.driver.find_element_by_xpath(imgPath).click()
            bet49 = self.driver.find_element_by_xpath('//*[@id="11000"]/div/div[3]/button[1]')
            bet49.click()

            self.driver.switch_to.window(
                self.driver.window_handles[1])  # SWITCHING TO THE NEW POPUP WINDOW THAT CONTAINS THE GAMES
            self.driver.maximize_window()
            time.sleep(7)

    def LaunchDemo(self):  # THE DEMO PLAY GETS RENDERED DIRECTLY FROM HERE
        self.driver.get('https://logigames.bet9ja.com/Games/Launcher?gameId=11000&provider=0&sid=&pff=1&skin=201')
        time.sleep(2)

        HILO = self.driver.find_element_by_xpath(
            "/html/body/div[1]/div/div/div/main/div[2]/div[1]/a[2]")  # Selecting our choicest the HI-LO Tab
        time.sleep(3)
        HILO.click()
        self.ChoosingBetType()  # Choosing what form of game we the bot should play repetitively
        self.BrainBox()

    def LaunchGame(self, uname, pwd):  # FUNCTION THAT HANDLES THE LOGIN PROCESS THROUGH TO THE GAME PLAY
        self.username = uname
        self.password = pwd
        self.login()
        HILO = self.driver.find_element_by_xpath(
            "/html/body/div[1]/div/div/div/main/div[2]/div[1]/a[2]")  # Selecting our choicest the HI-LO Tab
        time.sleep(3)
        HILO.click()
        self.ChoosingBetType()  # Choosing what form of game we the bot should play repetitively
        self.BrainBox()

    def LastResultType(self, sumOfBalls):  # DETERMINING WHETHER A ROUND IS EITHER LOW HI OR MID
        Driver = self.driver
        result = ""
        a = {range(21, 149): "LO", range(149, 152): "MID", range(152, 280): "HI"}
        for key in a:
            if sumOfBalls in key:
                result = a[key]
        return result

    def TimePrecision(self):  # GETTING THE EXACT TIME AND RETURNING THE VALUE NIN INTEGER
        value = self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div/footer/div[2]/div[4]/div/div/div').text
        return int(value)

    def sum_Of_Last_Result(self):  # GETTING THE SUM OF TOTAL BALLS RETURNED AND CONVERTING IT TO INTEGER
        total = self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div/main/div[1]/div[5]/div[2]/span').text
        self.currentRound = self.driver.find_element_by_xpath(
            "/html/body/div[1]/div/div/div/footer/div[2]/div[1]/div/div[2]").text
        try:  # CLICKING ON REFRESH TO REFRESH THE BALANCE AND GETTING THE VALUE IN ACCOUNT BALANCE
            refresh = self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div/header/div/div[2]/div[3]')
            refresh.click()
            self.balance = self.driver.find_element_by_xpath(
                '/html/body/div[1]/div/div/div/header/div/div[2]/div[1]/span').text
        except Exception as g:
            print(g)
            pass
        return int(total)

    def ChoosingBetType(self):
        Driver = self.driver
        if self.Type == 'HI':
            Driver.find_element_by_xpath(
                "/html/body/div[1]/div/div/div/main/div[2]/div[2]/div[1]/div[1]/div[2]/div/div/div[1]").click()
        elif self.Type == 'MID':
            Driver.find_element_by_xpath(
                "/html/body/div[1]/div/div/div/main/div[2]/div[2]/div[1]/div[1]/div[2]/div/div/div[2]").click()
        elif self.Type == 'LO':
            Driver.find_element_by_xpath(
                "/html/body/div[1]/div/div/div/main/div[2]/div[2]/div[1]/div[1]/div[2]/div/div/div[3]").click()

    def refresh(self):
        try:
            time.sleep(1)
            self.driver.refresh()
            time.sleep(2)
            self.driver.find_element_by_xpath("/html/body/div[1]/div/div/div/main/div[2]/div[1]/a[2]").click()
            self.ChoosingBetType()
        except Exception:
            self.driver.refresh()
            time.sleep(2)
            self.driver.find_element_by_xpath("/html/body/div[1]/div/div/div/main/div[2]/div[1]/a[2]").click()
            self.ChoosingBetType()

    def GamePlayAmount(self, Naira):
        Driver = self.driver
        TextArea = Driver.find_element_by_xpath(
            "/html/body/div[1]/div/div/div/main/div[2]/div[2]/div[3]/div/div[2]/div[1]/div[1]/input")
        time.sleep(2)
        TextArea.send_keys(Keys.CONTROL, 'a')
        time.sleep(2)
        TextArea.send_keys(Naira)

    def WinReset(self):
        self.profit += self.LostButWinning
        self.LostButWinning = 0
        self.profit += 50
        self.pro = self.profit
        self.lost = 0
        self.PrevAmount = 0
        self.Loosing_STREAK = 0
        self.status = "WON"
        print(self.status)
        print(F"TOTAL PROFIT MADE: +₦{self.profit}")
        print(F"TOTAL BALANCE: ₦{self.balance}")
        self.logrow[8] = "₦" + str(self.profit)  # AmtWon
        self.logrow[9] = "₦" + str(self.balance)  # TotalBalance
        self.save_to_database()
        self.MASANIELLO_SHEET[f'C{self.cell}'].value = "W"
        self.populateTable()

    def do_This_When_Loosing(self):
        self.won = 0
        self.LostButWinning += 50
        self.lost += self.stake
        self.Loosing_STREAK += 1
        self.status = "LOST"
        print(self.status)
        print("TOTAL LOST MADE: -₦", self.lost)
        print(F"TOTAL BALANCE: ₦{self.balance}")

        self.logrow[7] = "-₦" + str(self.lost)  # AmtLost
        self.logrow[8] = "₦" + str(self.pro)  # AmtWon
        self.logrow[9] = "₦" + str(self.balance)  # TotalBalance
        self.save_to_database()
        self.MASANIELLO_SHEET[f'C{self.cell}'].value = "L"
        self.populateTable()

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
        self.timepre = self.TimePrecision()
        self.logrow[3] = str(self.timepre)  # "TimePlaced"
        time.sleep(2)
        self.X = True
        while self.X:
            if self.TimePrecision() > 0:
                self.TimePrecision()
            elif self.TimePrecision() == 0:
                time.sleep(9)
                self.X = False
                break

    def click_on_Last_result_Type(self):
        if self.LastResultType(self.sum_Of_Last_Result()) == "HI" or self.LastResultType(
                self.sum_Of_Last_Result()) == "MID":
            self.Type = "HI"
            self.driver.find_element_by_xpath(
                "/html/body/div[1]/div/div/div/main/div[2]/div[2]/div[1]/div[1]/div[2]/div/div/div[1]").click()
        elif self.LastResultType(self.sum_Of_Last_Result()) == "LO":
            self.Type = "LO"
            self.driver.find_element_by_xpath(
                "/html/body/div[1]/div/div/div/main/div[2]/div[2]/div[1]/div[1]/div[2]/div/div/div[3]").click()

    def print_and_Log(self):
        self.Time = str(time.asctime())
        print("__" * 22)
        print(f"[{self.currentRound.upper()}]")
        print("__" * 22)
        print("\n[", self.Time, "]")
        print(f"Last Result was: {self.Type}")
        print("Sum of last result is--->:", self.sum_Of_Last_Result())
        print("[Total Lost--->", self.lost, "| Loosing_STREAK---->", self.Loosing_STREAK, "]")
        print(f"HIGHEST LOOSING STREAK FOR TODAY IS: [{self.highestLoosingStreak}] \nSetting Amount...")

    def save_to_database(self):
        self.logrow[0] = self.currentRound.split(":")[1].strip()  # "BetID"
        self.logrow[1] = str(self.sum_Of_Last_Result())
        self.logrow[2] = str(self.Type)  # "BetType"
        self.logrow[4] = str(self.Loosing_STREAK)  # "LoosingStreak"
        self.logrow[5] = "₦" + str(self.stake)  # "InvestmentAmt"
        self.logrow[6] = str(self.status)  # Win_Loss
        self.logrow[12] = str(self.highestLoosingStreak)  # "HighestStreak"

        import datetime
        self.logrow[10] = str(datetime.datetime.today().strftime("%H:%M:%S"))  # CurrentTime
        self.logrow[11] = str(datetime.date.today().strftime("%d/%m/%Y"))  # CurrentDate

        self.savingTodb()

    def populateTable(self):
        import datetime
        self.MASANIELLO_SHEET[f'B{self.cell}'].value = str(self.a)
        self.MASANIELLO_SHEET[f'G{self.cell}'].value = self.LastResultType(self.sum_Of_Last_Result())
        self.MASANIELLO_SHEET[f'H{self.cell}'].value = str(self.currentRound.split(":")[1].strip())
        self.MASANIELLO_SHEET[f'E{self.cell}'].value = str(self.sum_Of_Last_Result())
        self.MASANIELLO_SHEET[f'D{self.cell}'].value = "₦" + str(self.stake)
        self.MASANIELLO_SHEET[f'J{self.cell}'].value = str(self.timepre)
        self.MASANIELLO_SHEET[f'K{self.cell}'].value = int(self.balance)
        self.MASANIELLO_SHEET[f'L{self.cell}'].value = str(datetime.datetime.today().strftime("%H:%M:%S"))
        self.MASANIELLO_SHEET[f'M{self.cell}'].value = str(datetime.date.today().strftime("%d/%m/%Y"))
        self.MASANIELLO_SHEET[f'N{self.cell}'].value = self.highestLoosingStreak
        self.a += 1
        print(self.MASANIELLO_SHEET[f'L{self.cell}'].value)

    def savingTodb(self):
        logrow = self.logrow
        # saving to database table
        conn = sqlite3.connect("ZIRA.db")
        c = conn.cursor()
        c.execute(
            "INSERT into ZiraLog (BetId,BallsReturned,BetType,TimePlaced,LoosingStreak,InvestmentAmt,Won_Lost,AmtLost,Profit,TotalBalance,CurrentTime,CurrentDate,HighestStreak) values(?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (logrow[0], logrow[1], logrow[2], logrow[3], logrow[4], logrow[5], logrow[6], logrow[7], logrow[8],
             logrow[9], logrow[10], logrow[11], logrow[12]))

        conn.commit()
        # reset the list
        self.logrow = ["", "", "", "", "", "", "", "-₦0", "", "", "", "", ""]

    def waiting(self):
        # saving to database table
        conn = sqlite3.connect("ZIRA.db")
        c = conn.cursor()
        c.execute(
            "INSERT into ZiraLog (BetId,BallsReturned,BetType,TimePlaced,LoosingStreak,InvestmentAmt,Won_Lost,AmtLost,Profit,TotalBalance,CurrentTime,CurrentDate,HighestStreak) values(?,?,?,?,?,?,?,?,?,?,?,?,?)",
            ("Waiting...", "Waiting...", "Waiting...", "Waiting...", "Waiting...", "Waiting...", "Waiting...",
             "Waiting...", "Waiting...",
             "Waiting...", "Waiting...", "Waiting...", "Waiting..."))

        conn.commit()
        # reset the list
        self.logrow = ["", "", "", "", "", "", "", "-₦0", "", "", "", "", ""]
        time.sleep(49 * 5)

        a = 5
        while a > 0:
            self.stake = (self.PrevAmount * 2) + (self.InitialAmount * 4)
            self.setting_dont_placingBets()
            self.following_the_trend_waiting()
            a -= 1
        self.profit += (self.InitialAmount * 5)

    def following_the_trend(self):
        if self.LastResultType(self.sum_Of_Last_Result()) == self.Type:
            self.WinReset()

        elif self.LastResultType(self.sum_Of_Last_Result()) != self.Type:
            self.click_on_Last_result_Type()
            self.do_This_When_Loosing()

    def following_the_trend_waiting(self):
        if self.LastResultType(self.sum_Of_Last_Result()) == self.Type:
            self.Loosing_STREAK = 0
            pass

        elif self.LastResultType(self.sum_Of_Last_Result()) != self.Type:
            self.Loosing_STREAK += 1
            pass

    def sticking_to_one_direction(self):
        if self.LastResultType(self.sum_Of_Last_Result()) == self.Type:
            self.WinReset()

        elif self.LastResultType(self.sum_Of_Last_Result()) != self.Type:
            self.do_This_When_Loosing()

    def placeBet(self):
        Driver = self.driver
        place = Driver.find_element_by_class_name("place-bet")
        place.click()
        print(f"INVESTMENT: ₦{self.stake}")
        self.timepre = self.TimePrecision()
        print("BET PLACED! AT EXACTLY", self.timepre, "\n")
        self.logrow[3] = str(self.timepre)  # "TimePlaced"
        time.sleep(2)
        self.X = True
        while self.X:
            if self.TimePrecision() > 0:
                self.TimePrecision()
            elif self.TimePrecision() == 0:
                time.sleep(10)
                self.X = False
                break

    def placeBet_ExceptionHandling(self):
        try:
            self.placeBet()
        except Exception:
            self.setting_and_placingBets()

    def DontplaceBet_ExceptionHandling(self):
        try:
            Driver = self.driver
        except Exception:
            pass

    def highest_streak(self):
        if self.Loosing_STREAK >= self.highestLoosingStreak:
            self.highestLoosingStreak = self.Loosing_STREAK

    def closingDriver(self):
        self.driver.close()

    def BrainBox(self):  # This is the Engine of the bot
        while True:
            if self.sum_Of_Last_Result() != 0:
                print("LOADING...")
                while True:
                    while 40 >= self.TimePrecision() >= 20:

                        if self.Loosing_STREAK <= 2:
                            self.print_and_Log()
                            self.cell += 1
                            if self.sum_Of_Last_Result() != 0:
                                self.stake = (self.PrevAmount * 2) + self.InitialAmount
                                self.setting_and_placingBets()
                                self.following_the_trend()
                                self.highest_streak()

                        elif self.Loosing_STREAK == 3:
                            self.print_and_Log()
                            self.sticking_to_one_direction()
                            self.following_the_trend_waiting()
                            self.highest_streak()

                        elif 4 <= self.Loosing_STREAK <= 20:
                            self.print_and_Log()
                            self.setting_dont_placingBets()
                            self.following_the_trend_waiting()
                            self.highest_streak()


def LaunchBot(uname, pwd, amount):
    while True:
        try:
            ZIRA(amount, "LO").LaunchGame(uname, pwd)
            # x.LaunchDemo()
        except Exception as q:
            print(q)
            time.sleep(60 * 60 * 25)
            break


if __name__ == '__main__':
    while True:
        try:
            LaunchBot(amount=50)
        except Exception as e:
            print(e)
            time.sleep(60 * 60)
            LaunchBot(amount=50)
