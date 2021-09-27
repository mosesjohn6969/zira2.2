import time
import sqlite3
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
        self.results = 0
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
        self.workbookObj = xlwings.Book("algo.xlsx")
        self.MASANIELLO_SHEET = self.workbookObj.sheets['MASANIELLO']

        self.capital = 50000
        self.total_event = 100
        self.guessed_events = 46
        self.odds = 2
        self.cellStake = 0

        self.count = 5
        self.currentround = 1

        self.params = [self.capital, self.total_event, self.guessed_events, self.odds]
        for i in self.params:
            self.MASANIELLO_SHEET[f"I{self.count}"].value = i
            self.count += 1

    def gettingAndSettingValues(self):
        cells = 5
        self.cellStake = cells
        a = 100
        b = 1
        c = 0

        while True:
            getStakeValue = round(self.MASANIELLO_SHEET[f'D{cells}'].value)
            getNextStakeValue = getStakeValue
            print(getStakeValue)
            while b < a and getNextStakeValue > 50:
                self.cellStake += 1
                li = ["W", "L"]
                self.MASANIELLO_SHEET[f'C{cells}'].value = random.choice(li)
                time.sleep(1)
                getNextStakeValue = round(self.MASANIELLO_SHEET[f'D{self.cellStake}'].value)
                print(getNextStakeValue)

                a -= 1
                cells += 1

            a = 100
            b = 1
            cells = 5
            self.cellStake = cells
            c += 1
            print(f"we got Here {c} times")
            for column in self.MASANIELLO_SHEET['C5:C104']:
                for cell in column:
                    cell.value = None
            time.sleep(2)
            return int(getNextStakeValue)

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
        total = input("Sum of Last Round: ")
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
        print(self.status)
        print(F"TOTAL PROFIT MADE: +₦{self.profit}")
        print(F"TOTAL BALANCE: ₦{self.balance}")
        self.logrow[8] = "₦" + str(self.profit)  # AmtWon
        self.logrow[9] = "₦" + str(self.balance)  # TotalBalance
        self.save_to_database()

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

        print(f"INVESTMENT: ₦{self.stake}")
        timepre = self.TimePrecision()
        self.logrow[3] = str(timepre)  # "TimePlaced"

    def click_on_Last_result_Type(self):
        if self.LastResultType(self.results) == "HI" or self.LastResultType(
                self.results) == "MID":
            self.Type = "HI"

        elif self.LastResultType(self.results) == "LO":
            self.Type = "LO"

    def print_and_Log(self):
        self.Time = str(time.asctime())
        print(f"[{self.currentRound.upper()}]")
        print("__" * 22)
        print("\n[", self.Time, "]")
        print(f"Last Result was: {self.Type}")
        print("Sum of last result is--->:", self.results)
        print("[Total Lost--->", self.lost, "| Loosing_STREAK---->", self.Loosing_STREAK, "]")
        print(f"HIGHEST LOOSING STREAK FOR TODAY IS: [{self.highestLoosingStreak}] ")
        print("__" * 22)

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

            if self.Loosing_STREAK <= 4:
                if self.sum_Of_Last_Result != 0:
                    self.stake = (self.PrevAmount * 2) + self.InitialAmount
                    self.sticking_to_one_direction()
                    self.highest_streak()

            elif self.Loosing_STREAK == 5:
                self.waiting()
                self.Type = "LO"
                self.stake = (self.PrevAmount * 2) + (self.InitialAmount * 10)
                self.sticking_to_one_direction()
                self.highest_streak()

            elif 6 <= self.Loosing_STREAK <= 10:
                self.stake = (self.PrevAmount * 2)
                self.sticking_to_one_direction()
                self.highest_streak()

            elif 11 <= self.Loosing_STREAK <= 20:
                self.stake = (self.PrevAmount * 2)
                self.sticking_to_one_direction()
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
