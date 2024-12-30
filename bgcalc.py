### PyQt app boilerplate for my own use

import sys #for terminating app
import json
from functools import partial
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLineEdit, QPushButton, QVBoxLayout, QTableWidget, QLabel #required classes

ERROR_MSG = "ERROR"
WINDOW_SIZE = 235
DISPLAY_HEIGHT = 35
BUTTON_SIZE = 40

class BG3CalcWindow(QMainWindow): #window display info
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Character Calculator")
        self.setFixedSize(WINDOW_SIZE, WINDOW_SIZE) #cannot resize while this is here
        self.generalLayout = QVBoxLayout() #simple box positioning of widgets
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout) #assigns layout to widgets
        self.setCentralWidget(centralWidget)
        self._createDisplay()
        self._createButtons()
    def _createDisplay(self):
        self.display = QLineEdit()
        self.display.setFixedHeight(DISPLAY_HEIGHT)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.generalLayout.addWidget(self.display)

        # Add first user input field with label
        self.label1 = QLabel("Field 1")
        self.generalLayout.addWidget(self.label1)
        self.userInput1 = QLineEdit()
        self.userInput1.setFixedHeight(DISPLAY_HEIGHT)
        self.userInput1.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.generalLayout.addWidget(self.userInput1)

        # Add second user input field with label
        self.label2 = QLabel("Field 2")
        self.generalLayout.addWidget(self.label2)
        self.userInput2 = QLineEdit()
        self.userInput2.setFixedHeight(DISPLAY_HEIGHT)
        self.userInput2.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.generalLayout.addWidget(self.userInput2)

    def _createButtons(self):
        self.buttonMap = {}
        buttonsLayout = QGridLayout()
        self.generalLayout.addLayout(buttonsLayout)

        # Add save button
        self.saveButton = QPushButton("Save")
        self.saveButton.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        self.saveButton.clicked.connect(self.saveInputData)
        self.generalLayout.addWidget(self.saveButton)

    def setDisplayText(self, text):
        self.display.setText(text)
        self.display.setFocus()
    def displayText(self):
        return self.display.text()
    def clearDisplay(self):
        self.setDisplayText("")

    def saveInputData(self):
        data = {
            "input1": self.userInput1.text(),
            "input2": self.userInput2.text()
        }
        with open("input_data.json", "w") as file:
            json.dump(data, file)

def main(): #startup function
    bg3calcApp = QApplication([])
    bg3calcWindow = BG3CalcWindow() #inits GUI
    bg3calcWindow.show() #loads GUI
    sys.exit(bg3calcApp.exec()) #run the actual events

class BG3Calc:
    def __init__(self, model, view):
        self._evaluate = model
        self._view = view
        self._connectSigs()

if __name__ == "__main__":
    main()