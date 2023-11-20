from PyQt6 import QtWidgets, uic,QtGui, QtCore
import sys


class UI(QtWidgets.QMainWindow):
    def __init__(self):
        super(UI,self).__init__()
        uic.loadUi("Account Details.ui",self)
        self.show()
        self.home_screen=None #need to intialize this window, else the other screen disappears very quickly
        self.Login_Button.clicked.connect(self.after_logging_in)

    def after_logging_in(self): #to load the ui when we press the login Button
        self.home_screen=QtWidgets.QMainWindow() #window is initialized to none in the init function
        uic.loadUi("HOME.ui",self.home_screen)
        self.home_screen.show()




app=QtWidgets.QApplication(sys.argv) #create an instance of QTwidgets.Qapplication
window=UI() #create an instance of our class
app.exec()