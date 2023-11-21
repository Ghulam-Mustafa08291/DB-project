from PyQt6 import QtWidgets, uic,QtGui, QtCore
import sys


class UI(QtWidgets.QMainWindow):
    def __init__(self):
        super(UI,self).__init__()
        uic.loadUi("Account Details.ui",self) #will show the login screen
        self.show() 
        self.home_screen=None #need to intialize this window, else the other screen disappears very quickly
        self.update_screen=None #initializing the window
        self.Login_Button.clicked.connect(self.after_logging_in)
        

    def after_logging_in(self): #to load the ui when we press the login Button, will show the home menu
        self.home_screen=QtWidgets.QMainWindow() #window is initialized to none in the init function
        uic.loadUi("HOME.ui",self.home_screen)
        self.home_screen.show()
        self.home_screen.pushButton_5.clicked.connect(self.after_clicking_updates) #when the updates button is clicked on the screen

    def after_clicking_updates(self): # shows the updates screen
        self.update_screen=QtWidgets.QMainWindow()
        uic.loadUi("Updates.ui",self.update_screen)
        self.update_screen.show()




app=QtWidgets.QApplication(sys.argv) #create an instance of QTwidgets.Qapplication
window=UI() #create an instance of our class
app.exec()