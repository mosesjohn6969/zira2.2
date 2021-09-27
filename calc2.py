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

        self.capital = 100000
        self.total_event = 100
        self.guessed_events = 46
        self.odds = 2

        # variables needed in the gettingAndSettingValues method
        self.cells = 5
        self.cellStake = self.cells
        self.a = 100
        self.b = 1
        self.c = 0
        self.w = 0

        self.count = 5
        self.currentround = 1

        self.params = [self.capital, self.total_event, self.guessed_events, self.odds]
        for i in self.params:
            self.MASANIELLO_SHEET[f"I{self.count}"].value = i
            self.count += 1

    def gettingAndSettingValues(self):  # getting the value in the D Column (the bet to be made)

        getStakeValue = round(self.MASANIELLO_SHEET[f'D{self.cells}'].value)
        getNextStakeValue = getStakeValue

        if self.b < self.a and getNextStakeValue > 50:  # running the logic only if the 100 rounds is still active and the stake value is not less than 50
            # moving unto the next cell
            self.cellStake += 1

            # passing in the result of the current round to the spread sheet to facilitate generation of the next stake value
            if self.LastResultType(self.results) == "HI" or self.LastResultType(self.results) == "MID":
                # self.Type = "HI"
                self.MASANIELLO_SHEET[f'C{self.cells}'].value = "L"

            elif self.LastResultType(self.results) == "LO":
                # self.Type = "LO"
                self.MASANIELLO_SHEET[f'C{self.cells}'].value = "W"
            # reducing the value of a (to indicate the round (from 100 downwards))
            self.a -= 1
            # incrementing the value of 'cells' so zira can move to the next cell in the D or C column of the excel file
            self.cells += 1
        else:
            print("\n\n")
            print("clearing values")
            print("\n\n")
            # resetting the variables to default values at the end of the 100 round flow
            self.a = 100
            self.b = 1
            self.cells = 5
            self.cellStake = self.cells
            # variable holding the number of times the application has successfully completed a 100 rounds
            self.c += 1
            print(f"we got Here {self.c} times")

            rand = ["HI", "LO"]
            self.Type = random.choice(rand)
            # clearing the values in all the C cells (win - loss info) so zira can start an new 100 rounds calculation
            for column in self.MASANIELLO_SHEET['C5:C104']:
                for cell in column:
                    cell.value = None

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
        import random
        # total = input("Sum of Last Round: ")
        time.sleep(2)
        rand = [50, 160, 140, 201, 112, 250, 150, 130, 160]
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
        if self.LastResultType(self.results) == "HI" or self.LastResultType(
                self.results) == "MID":
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
        if self.LastResultType(self.LastResultType(self.results)) == self.Type:
            self.WinReset()

        elif self.LastResultType(self.LastResultType(self.results)) != self.Type:
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
                    self.stake = self.gettingAndSettingValues()
                    self.sticking_to_one_direction()
                    self.highest_streak()

            elif self.Loosing_STREAK == 5:
                self.waiting()
                self.stake = self.gettingAndSettingValues()
                self.sticking_to_one_direction()
                self.highest_streak()

            elif 6 <= self.Loosing_STREAK <= 10:
                self.stake = self.gettingAndSettingValues()
                self.sticking_to_one_direction()
                self.highest_streak()

            elif 11 <= self.Loosing_STREAK <= 20:
                self.stake = self.gettingAndSettingValues()
                self.sticking_to_one_direction()
                self.highest_streak()


def LaunchBot(amount):
    while True:
        try:
            rand = ["HI", "LO"]
            type = random.choice(rand)
            ZIRA(amount, type).BrainBox()
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
