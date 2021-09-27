
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLineEdit, QComboBox, QTimeEdit, QDateEdit
from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from zira import ZIRA, validation, LaunchBot
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtGui
import PyQt5
import sys
import sqlite3

from PyQt5.QtWidgets import QMessageBox


class UI(QtWidgets.QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("Zira.ui", self)

        self.Run = self.findChild(QPushButton, "runBot")
        self.Demo = self.findChild(QPushButton, "demo")
        self.Stop = self.findChild(QPushButton, "stopBot")
        self.Log = self.findChild(QPushButton, "logbtn")
        self.User_Name = self.findChild(QLineEdit, "userName")
        self.Password = self.findChild(QLineEdit, "password")
        self.Amount = self.findChild(QComboBox, "amount")

        self.worker = WorkerThread()
        self.demoT = demoThread()
        self.Run.clicked.connect(self.RunBtnClicked)
        self.Demo.clicked.connect(self.DemoBtnClicked)
        self.Stop.clicked.connect(self.StopBtnClicked)
        self.Log.clicked.connect(self.LogBtnClicked)
        self.window = PyQt5.QtWidgets.QMainWindow()

        # self.User_Name.setText("tolumore")
        # self.Password.setText("12drk34")
        self.show()

    @pyqtSlot()
    def RunBtnClicked(self):
        self.runBot.setIcon(QIcon())
        # self.runBot.setStyleSheet("qproperty-icon: url()")
        font = QtGui.QFont()
        font.setPointSize(15)
        self.runBot.setFont(font)
        self.runBot.setText("Running...")
        self.worker.setValues(self.userName.text(), self.password.text(), int(self.Amount.currentText()))
        self.worker.start()

    @pyqtSlot()
    def DemoBtnClicked(self):
        self.demo.setIcon(QIcon())
        font = QtGui.QFont()
        font.setPointSize(15)
        self.demo.setFont(font)
        self.demo.setText("Running...")
        self.demoT.setValues(int(self.Amount.currentText()))
        self.demoT.start()

    @pyqtSlot()
    def StopBtnClicked(self):
        if self.worker.isRunning():
            self.worker.stop()
        if self.demoT.isRunning():
            self.demoT.stop()

        print("stopping thread")

    @pyqtSlot()
    def LogBtnClicked(self):
        self.window = LogPage()


class WorkerThread(QtCore.QThread):
    def __init__(self, parent=None):
        super(WorkerThread, self).__init__(parent)
        self.username = None
        self.password = None
        self.amount = None

    def stop(self):
       self.terminate()

    def setValues(self, setUsername, setPassword, setAmount):
        self.username = setUsername
        self.password = setPassword
        self.amount = setAmount
    # def messageBox(self):
    #     msg = QMessageBox()
    #     msg.setWindowTitle("Error")
    #     msg.setWindowIcon("exit.png")
    #     msg.setText("Wrong Information")
    #     msg.setIcon(QMessageBox.Critical)
    #     x = msg.exec_()

    def real(self):
        ZIRA(50, "LO").LaunchDemo()

    def run(self):
        if validation(self.username, self.password):
            try:
                LaunchBot(self.username, self.password,self.amount)
            except Exception as e:
                print(e)
                if "about:neterror" in str(e):
                    print("There is no internet connection")
                elif "Process unexpectedly closed" in str(e):
                    print("Browser was unexpectedly closed")


class demoThread(QtCore.QThread):
    def __init__(self, parent=None):
        super(demoThread, self).__init__(parent)
        self.amount = None

    def setValues(self, setAmount):
        self.amount = setAmount

    def stop(self):
        self.terminate()

    def run(self):
        try:
            ZIRA(self.amount, "LO").LaunchDemo()
        except Exception as e:
            print(e)
            if "about:neterror" in str(e):
                print("There is no internet connection")
            elif "Process unexpectedly closed" in str(e):
                print("Browser was unexpectedly closed")



class LogPage(QtWidgets.QMainWindow):
    def __init__(self):
        super(LogPage, self).__init__()
        uic.loadUi("log.ui", self)
        self.updateTable = self.findChild(QPushButton, "updateTable")
        self.updateTable.clicked.connect(self.populateTable)
        self.newTable = self.findChild(QPushButton, "newTable")
        self.newTable.clicked.connect(self.newTables)
        self.TimeEdit = self.findChild(QTimeEdit, "timeEdit")
        self.DateEdit = self.findChild(QDateEdit, "dateEdit")

        # self.SearchRecord = self.findChild(QPushButton, "searchRecords")
        self.searchRecords.clicked.connect(self.searchingForRecords)
        # self.workerD = WorkerThread()

        # self.printing = self.findChild(QPushButton, "printDialog")
        # self.printing.clicked.connect(self.printDialog)

        self.show()
        self.populateTable()

    def searchingForRecords(self):
        db = sqlite3.connect("ZIRA.db")
        cur = db.cursor()
        # print("Slab",self.DateEdit.date().toPyDate(), self.TimeEdit.time().toPyTime())
        date = str(self.DateEdit.date().toPyDate())
        date = date.split('-')
        for i in range(len(date) - 1):
            if date[i] == "-":
                date[i] = "/"
        lst_date = list(reversed(date))
        lst_date.insert(1, "/")
        lst_date.insert(3, "/")
        str_date = ""
        for el in lst_date:
            str_date += el
        date = str_date
        # date = date.replace('-','/')
        info = cur.execute(f"SELECT * FROM ZiraLog  WHERE CurrentDate like '{date}'")
        result = info.fetchall()
        # print(result)
        if len(result) < 1:
            pops = QMessageBox()
            pops.setWindowTitle("Record does not exist")
            pops.setText("There are no records on this date")
            x = pops.exec_()
        else:
            self.tableWidget.setRowCount(len(result))
            row = 0
            for individualLog in result:
                self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(individualLog[0])))
                self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(individualLog[1])))
                self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(individualLog[2])))
                self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(individualLog[3])))
                self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(individualLog[4])))
                self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(str(individualLog[5])))
                self.tableWidget.setItem(row, 6, QtWidgets.QTableWidgetItem(str(individualLog[6])))
                self.tableWidget.setItem(row, 7, QtWidgets.QTableWidgetItem(str(individualLog[7])))
                self.tableWidget.setItem(row, 8, QtWidgets.QTableWidgetItem(str(individualLog[8])))
                self.tableWidget.setItem(row, 9, QtWidgets.QTableWidgetItem(str(individualLog[9])))
                self.tableWidget.setItem(row, 10, QtWidgets.QTableWidgetItem(str(individualLog[10])))
                self.tableWidget.setItem(row, 11, QtWidgets.QTableWidgetItem(str(individualLog[11])))
                self.tableWidget.setItem(row, 12, QtWidgets.QTableWidgetItem(str(individualLog[12])))
                self.tableWidget.setItem(row, 13, QtWidgets.QTableWidgetItem(str(individualLog[13])))
                row = row + 1

    def newTables(self):
        self.populateTable()

        db = sqlite3.connect("ZIRA.db")
        cur = db.cursor()
        cur.execute("DROP TABLE IF EXISTS  ZiraLog ")
        cur.execute("CREATE table ZiraLog (EntryId INTEGER PRIMARY KEY,BetId TEXT,BallsReturned TEXT, BetType TEXT,TimePlaced TEXT,LoosingStreak TEXT,InvestmentAmt TEXT,Won_Lost TEXT,AmtLost TEXT,Profit TEXT,TotalBalance TEXT,CurrentTime TEXT,CurrentDate TEXT,HighestStreak TEXT)")

        db.commit()
        self.populateTable()

    def populateTable(self):
        print("updating table")
        conn = sqlite3.connect("ZIRA.db")
        c = conn.cursor()
        # getting the values from table
        query = c.execute("SELECT * from ZiraLog")
        content = query.fetchall()
        # editing the Log Window
        self.logWindow.setRowCount(len(content))

        row = 0
        for individualLog in content:
            self.logWindow.setItem(row, 0, QtWidgets.QTableWidgetItem(str(individualLog[0])))
            self.logWindow.setItem(row, 1, QtWidgets.QTableWidgetItem(str(individualLog[1])))
            self.logWindow.setItem(row, 2, QtWidgets.QTableWidgetItem(str(individualLog[2])))
            self.logWindow.setItem(row, 3, QtWidgets.QTableWidgetItem(str(individualLog[3])))
            self.logWindow.setItem(row, 4, QtWidgets.QTableWidgetItem(str(individualLog[4])))
            self.logWindow.setItem(row, 5, QtWidgets.QTableWidgetItem(str(individualLog[5])))
            self.logWindow.setItem(row, 6, QtWidgets.QTableWidgetItem(str(individualLog[6])))
            self.logWindow.setItem(row, 7, QtWidgets.QTableWidgetItem(str(individualLog[7])))
            self.logWindow.setItem(row, 8, QtWidgets.QTableWidgetItem(str(individualLog[8])))
            self.logWindow.setItem(row, 9, QtWidgets.QTableWidgetItem(str(individualLog[9])))
            self.logWindow.setItem(row, 10, QtWidgets.QTableWidgetItem(str(individualLog[10])))
            self.logWindow.setItem(row, 11, QtWidgets.QTableWidgetItem(str(individualLog[11])))
            self.logWindow.setItem(row, 12, QtWidgets.QTableWidgetItem(str(individualLog[12])))
            self.logWindow.setItem(row, 13, QtWidgets.QTableWidgetItem(str(individualLog[13])))
            row = row + 1

    def printDialog(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            self.logWindow.print_(printer)
        self.workerD.start()


class printThread(QtCore.QThread):
    def __init__(self, parent=None):
        super(printThread, self).__init__(parent)

    def run(self):
        LogPage().printDialog()


app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()

