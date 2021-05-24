import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from naver_google_crawling import naver,google
form_class = uic.loadUiType(r"D:\crawling\crawling.ui")[0]

class WindowClass(QMainWindow, form_class) :
    def __init__(self):
    
        super().__init__()
        self.setupUi(self)
        self.check = ''
        self.keyword = ''''''
        self.radioButton.clicked.connect(self.radio_naver)
        self.radioButton2.clicked.connect(self.radio_google)
        
        self.Search.clicked.connect(self.crawling)

    def radio_naver(self):
        self.check = 'naver'
        
    def radio_google(self):
        self.check = 'google'
        
    def input_keyword(self):
        self.keyword = self.textEdit.toPlainText()
    def crawling(self):
        self.keyword = self.textEdit.toPlainText()
        if self.check == 'naver':
            naver(self.keyword)
        else:
            google(self.keyword)
if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
