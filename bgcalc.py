### PyQt app boilerplate for my own use

import sys #for terminating app
from functools import partial
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLineEdit, QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem #required classes

ERROR_MSG = "ERROR"
WINDOW_SIZE = 235
DISPLAY_HEIGHT = 35
BUTTON_SIZE = 40

class BG3CalcWindow(QMainWindow): #window display info
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BG3Calc")
        self.setFixedSize(WINDOW_SIZE, WINDOW_SIZE) #cannot resize while this is here
        self.generalLayout = QVBoxLayout() #simple box positioning of widgets
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout) #assigns layout to widgets
        self.setCentralWidget(centralWidget)
        self._createDisplay()
        self._createButtons()
        self._createMonthTable()  # Add this line to initialize the table

    def _createDisplay(self):
        self.display = QLineEdit()
        self.display.setFixedHeight(DISPLAY_HEIGHT)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.generalLayout.addWidget(self.display)
    def _createButtons(self):
        self.buttonMap = {}
        buttonsLayout = QGridLayout()
        keyBoard = [
            ["7", "8", "9", "/", "C"],
            ["4", "5", "6", "*", "("],
            ["1", "2", "3", "-", ")"],
            ["0", "00", ".", "+", "="],
        ]
        for row, keys in enumerate(keyBoard):
            for col, key in enumerate(keys):
                self.buttonMap[key] = QPushButton(key)
                self.buttonMap[key].setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
                buttonsLayout.addWidget(self.buttonMap[key], row, col)
        self.generalLayout.addLayout(buttonsLayout)
    def _createMonthTable(self):
        self.monthTable = QTableWidget(3, 4)  # 3 rows, 4 columns
        months = [
            "January", "February", "March", "April",
            "May", "June", "July", "August",
            "September", "October", "November", "December"
        ]
        for i, month in enumerate(months):
            row = i // 4
            col = i % 4
            self.monthTable.setItem(row, col, QTableWidgetItem(month))
        self.generalLayout.addWidget(self.monthTable)
    def setDisplayText(self, text):
        self.display.setText(text)
        self.display.setFocus()
    def displayText(self):
        return self.display.text()
    def clearDisplay(self):
        self.setDisplayText("")

def main(): #startup function
    bg3calcApp = QApplication([])
    bg3calcWindow = BG3CalcWindow() #inits GUI
    bg3calcWindow.show() #loads GUI
    BG3Calc(model=evaluate, view=bg3calcWindow)
    sys.exit(bg3calcApp.exec()) #run the actual events

def evaluate(expr):
    try:
        result = str(eval(expr, {}, {}))
    except Exception:
        result = ERROR_MSG
    return result

class BG3Calc:
    def __init__(self, model, view):
        self._evaluate = model
        self._view = view
        self._connectSigs()
    def _calcResult(self):
        result = self._evaluate(expr=self._view.displayText())
        self._view.setDisplayText(result)
    def _buildExpr(self, subExpr):
        if self._view.displayText() == ERROR_MSG:
            self._view.clearDisplay()
        expr = self._view.displayText() + subExpr
        self._view.setDisplayText(expr)
    def _connectSigs(self):
        for symb, button in self._view.buttonMap.items():
            if symb not in {"=", "C"}:
                button.clicked.connect(
                    partial(self._buildExpr, symb)
                )
        self._view.buttonMap["="].clicked.connect(self._calcResult)
        self._view.display.returnPressed.connect(self._calcResult)
        self._view.buttonMap["C"].clicked.connect(self._view.clearDisplay)



if __name__ == "__main__":
    main()