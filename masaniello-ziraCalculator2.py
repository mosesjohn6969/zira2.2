import time
import sqlite3
import datetime
import random
import openpyxl
import xlwings


class ZIRA:  # ZIRA CLASS THAT CONTAINS THE BRAIN BOX
    def __init__(self, firstAmount, type):
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
        self.results = 0
        self.Type = type
        self.username = ""
        self.password = ""
        self.investment = ""
        self.highestLoosingStreak = 0
        self.InitialAmount = firstAmount
        self.logrow = ["", "", "", "", "", "", "", "-₦0", "", "", "", "", ""]
        self.workbookObj = xlwings.Book("algo.xlsx")
        self.MASANIELLO_SHEET = self.workbookObj.sheets['MASANIELLO']

        self.capital = 50000
        self.total_event = 100
        self.guessed_events = 47
        self.odds = 2

        # variables needed in the gettingAndSettingValues method
        self.cells = 5
        self.bal = 5
        self.cellStake = self.cells
        self.getBalance = 0
        self.a = 100
        self.b = 0
        self.c = 0
        self.w = 0

        self.eventsWon = 0
        self.getBalance = 0
        self.gettingAndSettingStatus = "false"
        self.getNextStakeValue = 0

        self.count = 5
        self.currentround = 1

        self.params = [self.capital, self.total_event, self.guessed_events, self.odds]
        for i in self.params:
            self.MASANIELLO_SHEET[f"S{self.count}"].value = i
            self.count += 1

        self.profitByPercent = round(self.MASANIELLO_SHEET[f'S{11}'].value)
        print(self.profitByPercent)

    def populateTable(self):
        self.MASANIELLO_SHEET[f'G{self.cells}'].value = self.LastResultType(self.results)
        self.MASANIELLO_SHEET[f'H{self.cells}'].value = self.currentRound.split(":")[1].strip()
        self.MASANIELLO_SHEET[f'I{self.cells}'].value = self.results
        self.MASANIELLO_SHEET[f'J{self.cells}'].value = self.TimePrecision()
        self.MASANIELLO_SHEET[f'K{self.cells}'].value = self.balance
        self.MASANIELLO_SHEET[f'L{self.cells}'].value = str(datetime.datetime.today().strftime("%H:%M:%S"))
        self.MASANIELLO_SHEET[f'M{self.cells}'].value = str(datetime.date.today().strftime("%d/%m/%Y"))
        self.MASANIELLO_SHEET[f'N{self.cells}'].value = self.highestLoosingStreak

    def gettingAndSettingValues(self):  # getting the value in the D Column (the bet to be made)  gettingStakeAmountAndBalance
        getStakeValue = round(self.MASANIELLO_SHEET[f'D{self.cells}'].value)
        self.getNextStakeValue = getStakeValue

        self.gettingAndSettingStatus = "true"
        return int(self.getNextStakeValue)

    def settingWinOrLoseAndRefreshing(self):  # getting the value in the D Column (the bet to be made)
        if self.b < (self.a-1) and self.gettingAndSettingValues() > int(0.8 * self.capital / 100) and self.getBalance <= self.profitByPercent and self.eventsWon != 46:  # running the logic only if the 100 rounds is still active and the stake value is not less than 50
            # moving unto the next cell
            self.cellStake += 1
            print("we got here in excel")

            # passing in the result of the current round to the spread sheet to facilitate generation of the next stake value

            if self.LastResultType(self.results) == "MID":
                self.MASANIELLO_SHEET[f'C{self.cells}'].value = "L"
                self.populateTable()
                time.sleep(1.1)

            elif self.LastResultType(self.results) == self.Type:
                self.MASANIELLO_SHEET[f'C{self.cells}'].value = "W"
                self.populateTable()
                time.sleep(1.2)

            elif self.LastResultType(self.results) != self.Type:
                self.MASANIELLO_SHEET[f'C{self.cells}'].value = "L"
                self.populateTable()
                time.sleep(1.2)

            # reducing the value of a (to indicate the round (from 100 downwards))
            self.a -= 1
            # incrementing the value of 'cells' so zira can move to the next cell in the D or C column of the excel file
            self.cells += 1
        else:
            print("\n\n")
            print("clearing values")
            print("\n\n")
            self.Loosing_STREAK = 0
            self.bal = 5

            self.getBalance = 0
            self.gettingAndSettingStatus = "false"
            self.a = 100
            self.b = 0
            self.cells = 5
            self.cellStake = self.cells
            # variable holding the number of times the application has successfully completed a 100 rounds
            self.eventsWon = 0
            self.c += 1
            print(f"we got Here {self.c} times")
            the_cells = ['C', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N']
            for i in the_cells:
                for column in self.MASANIELLO_SHEET[f'{i}5:{i}104']:
                    for cell in column:
                        cell.value = None
            # clearing the values in all the C cells (win - loss info) so zira can start an new 100 rounds calculation
            # for column in self.MASANIELLO_SHEET['C5:C104']:
            #     for cell in column:
            #         cell.value = None
            #
            #
            #
            # for column in self.MASANIELLO_SHEET['G5:G104']:
            #     for cell in column:
            #         cell.value = None
            # for column in self.MASANIELLO_SHEET['H5:H104']:
            #     for cell in column:
            #         cell.value = None
            # for column in self.MASANIELLO_SHEET['I5:I104']:
            #     for cell in column:
            #         cell.value = None
            # for column in self.MASANIELLO_SHEET['J5:J104']:
            #     for cell in column:
            #         cell.value = None
            # for column in self.MASANIELLO_SHEET['K5:K104']:
            #     for cell in column:
            #         cell.value = None
            # for column in self.MASANIELLO_SHEET['L5:L104']:
            #     for cell in column:
            #         cell.value = None
            # for column in self.MASANIELLO_SHEET['M5:M104']:
            #     for cell in column:
            #         cell.value = None
            # for column in self.MASANIELLO_SHEET['N5:O104']:
            #     for cell in column:
            #         cell.value = None

        try:
            print(f"events WON:{self.eventsWon}, available balance: {self.getBalance}")
            print(
                f"cell:{self.cells}, getNextStakeValue: {self.getNextStakeValue}, bal cell: {self.bal}, getBalance: {self.getBalance}")
            self.eventsWon = round(self.MASANIELLO_SHEET[f'S{16}'].value)
            self.getBalance = round(self.MASANIELLO_SHEET[f'F{self.bal}'].value)
            self.bal = self.cells

        except Exception as v:
            print(v, "BUT THIS BUG WAS HANDLED")
            pass

    def LastResultType(self, sumOfBalls):
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
        import random
        # total = input("Sum of Last Round: ")
        time.sleep(2)
        rand = [41, 185, 140, 150, 200, 137, 159, 126, 179, 132, 167, 139, 196, 127, 190, 124, 157, 111, 163]
        total = random.choice(rand)
        self.currentRound = "Current draw: 2469102"

        try:
            self.balance = 100000
        except Exception as g:
            print(g)
            pass
        return int(total)

    def ChoosingBetType(self):
        if self.Type == 'HI':
            pass
        elif self.Type == 'MID':
            pass
        elif self.Type == 'LO':
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
        print(f"TOTAL LOST: -₦", self.profit)
        print(f"INVESTMENT: ₦{self.stake}"f" |TOTAL BALANCE: ₦{self.balance}")
        self.logrow[8] = "₦" + str(self.profit)  # AmtWon
        self.logrow[9] = "₦" + str(self.balance)  # TotalBalance
        self.save_to_database()
        print("__" * 28)

    def do_This_When_Loosing(self):
        self.won = 0
        self.LostButWinning += 50
        self.lost += self.stake
        self.Loosing_STREAK += 1
        self.status = "LOST"
        print(f"TOTAL LOST: -₦", self.lost)
        print(f"INVESTMENT: ₦{self.stake}"f" |TOTAL BALANCE: ₦{self.balance}")

        self.logrow[7] = "-₦" + str(self.lost)  # AmtLost
        self.logrow[8] = "₦" + str(self.pro)  # AmtWon
        self.logrow[9] = "₦" + str(self.balance)  # TotalBalance
        self.save_to_database()

        timepre = self.TimePrecision()
        self.logrow[3] = str(timepre)  # "TimePlaced"
        print("__" * 28)

    def click_on_Last_result_Type(self):
        if self.LastResultType(self.results) == "MID":

            if self.Type == "LO":
                self.Type = "HI"
            elif self.Type == "HI":
                self.Type = "LO"

        elif self.LastResultType(self.results) == "HI":
            self.Type = "HI"

        elif self.LastResultType(self.results) == "LO":
            self.Type = "LO"

    def print_and_Log(self):
        self.Time = str(time.asctime())
        print(f"[{self.currentRound.upper()}", self.Time, "]")
        print("__" * 28, "\n")
        print(f"ROUND {self.status}| LAST RESULT:", self.results, f"|{self.LastResultType(self.results)}")
        print("[LOST:₦", self.lost, "| LOOSING STREAK:", self.Loosing_STREAK,
              f"| HIGHEST LOOSING: [{self.highestLoosingStreak}] ")

    def save_to_database(self):
        self.logrow[0] = self.currentRound.split(":")[1].strip()  # "BetID"
        self.logrow[1] = str(self.results)
        self.logrow[2] = str(self.Type)  # "BetType"
        self.logrow[4] = str(self.Loosing_STREAK)  # "LoosingStreak"
        self.logrow[5] = "₦" + str(self.stake)  # "InvestmentAmt"
        self.logrow[6] = str(self.status)  # Win_Loss
        self.logrow[12] = str(self.highestLoosingStreak)  # "HighestStreak"

        import datetime
        self.logrow[10] = str(datetime.datetime.today().strftime("%H:%M:%S"))  # CurrentTime
        self.logrow[11] = str(datetime.date.today().strftime("%d/%m/%Y"))  # CurrentDate

        self.savingTodb()

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
        self.profit += (self.InitialAmount * 10)

    def following_the_trend(self):
        if self.LastResultType(self.results) == self.Type:
            self.WinReset()

        elif self.LastResultType(self.results) != self.Type:
            self.click_on_Last_result_Type()
            self.do_This_When_Loosing()

    def sticking_to_one_direction(self):
        if self.LastResultType(self.results) == self.Type:
            self.WinReset()

        elif self.LastResultType(self.results) != self.Type:
            self.do_This_When_Loosing()

    def highest_streak(self):
        if self.Loosing_STREAK >= self.highestLoosingStreak:
            self.highestLoosingStreak = self.Loosing_STREAK

    def BrainBox(self):  # This is the Engine of the bot
        while 40 >= self.TimePrecision() >= 20:
            self.print_and_Log()
            self.results = self.sum_Of_Last_Result()

            if self.gettingAndSettingStatus == "true":  # checking if the value has already been gotten from the excel file
                self.settingWinOrLoseAndRefreshing()  # inputting the last round status into the excel file
                self.gettingAndSettingStatus = "false"

            if self.Loosing_STREAK <= 1:
                if self.sum_Of_Last_Result != 0:
                    self.stake = self.gettingAndSettingValues()
                    self.following_the_trend()
                    self.highest_streak()

            elif 2 <= self.Loosing_STREAK <= 10:
                print("we got here")
                self.following_the_trend()
                self.highest_streak()

            elif 11 <= self.Loosing_STREAK <= 120:
                self.stake = self.gettingAndSettingValues()
                self.following_the_trend()
                self.highest_streak()


def LaunchBot(amount):
    while True:
        try:
            ZIRA(amount, "LO").BrainBox()
            # x=LaunchDemo()
        except Exception as a:
            print(a)
            break


if __name__ == '__main__':
    while True:
        try:
            LaunchBot(50)
        except Exception as e:
            print(e)
            time.sleep(60 * 60)
            LaunchBot(50)
