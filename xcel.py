import xlwings as xw
import random
class masaniello():
    def __init__(self):
        self.wbxl =xw.Book('algo.xlsx')
        self.sheet = self.wbxl.sheets['MASANIELLO']
        self.intial_cap = 1000
        self.total_ev = 100
        self.guessed_ev = 46
        self.odds = 2

        self.count = 5
        self.currentround = 1

        self.params = [self.intial_cap,self.total_ev,self.guessed_ev,self.odds]
        for i in self.params:
            self.sheet.range(f"I{self.count}").value = i
            self.count +=1
        self.wbxl.save()
    def getFirstStake(self):
        return round(self.sheet.range("D5").value)

    def currentCellValue(self):
        return self.currentround+4

    def nextStake(self, wl):
        if len(wl) != "":
            if wl == "W":
                self.sheet.range(f"C{self.currentCellValue()}").value = "W"
            elif wl == "L":
                self.sheet.range(f"C{self.currentCellValue()}").value = "L"

        self.currentround += 1
        return round(self.sheet.range(f"D{self.currentCellValue()}").value)

    def close(self):
        self.wbxl.close()


book = masaniello()
print(book.getFirstStake())
li = ["W","L"]
for i in range(10):
    print(book.nextStake(random.choice(li)))