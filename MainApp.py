from PyQt6 import QtWidgets, uic,QtGui, QtCore
import sys
import pyodbc
from PyQt6.QtWidgets import QTableWidgetItem

#connecting the database below
server="LAPTOP-4OMLOR40"
database="AnimeManagement"
use_windows_authentication=True
username=""
password=""


if use_windows_authentication:
    connection_string=f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"
else:
   connection_string= f"Driver={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"



connection=pyodbc.connect(connection_string)

cursor=connection.cursor()
#cursor.execute("select * from Anime")

# rows=cursor.fetchall()

# for row in rows:
#     print(row)





class UI(QtWidgets.QMainWindow):
    def __init__(self):
        super(UI,self).__init__()
        uic.loadUi("Login.ui",self) #will show the login screen
        self.show() 
        self.home_screen=None #need to intialize this window, else the other screen disappears very quickly
        self.update_screen=None #initializing the window
        self.logout_screen=None #same screen as that of account details, when one logs out
        self.SignUpScreen=None #initializing the window
        self.MyContentScreen=None
        self.comments_and_details_screen=None
        self.Login_Button.clicked.connect(self.after_logging_in)
        self.SignUpButton.clicked.connect(self.load_signup_screen)
        
        

    def after_logging_in(self): #to load the ui when we press the login Button, will show the home menu
        self.home_screen=QtWidgets.QMainWindow() #window is initialized to none in the init function
        uic.loadUi("HOME.ui",self.home_screen)
        self.home_screen.show()
        self.home_screen.pushButton_5.clicked.connect(self.after_clicking_updates) #when the updates button is clicked on the screen'
        self.home_screen.pushButton.clicked.connect(self.search_by_name) #when the search button is clicked on the home screen
        self.home_screen.pushButton_3.clicked.connect(self.show_login_screen)
        self.home_screen.pushButton_6.clicked.connect(self.load_MyContent_screen)
        self.home_screen.pushButton_8.clicked.connect(self.load_Comments_and_details)
        
            


    def after_clicking_updates(self): # shows the updates screen
        self.update_screen=QtWidgets.QMainWindow()
        uic.loadUi("Updates.ui",self.update_screen)
        self.update_screen.show()
        self.update_screen.pushButton_3.clicked.connect(self.show_login_screen)
        self.update_screen.pushButton_6.clicked.connect(self.load_MyContent_screen)
        self.update_screen.pushButton_8.clicked.connect(self.after_logging_in)

    def search_by_name(self): #for searching through the name in the HOME screen ui
        name=self.home_screen.lineEdit.text()
        #print(name)
        cursor.execute(f"select * from Series where SeriesName='{name}'")
        rows=cursor.fetchall()

        for row in range(len(rows)):
            for j in range(len(rows[row])):
                item=QTableWidgetItem(str(rows[row][j]))
                self.home_screen.tableWidget.setItem(row,j,item)
                print(row)
            

    def show_login_screen(self):
        self.logout_screen=QtWidgets.QMainWindow() #window is initialized to none in the init function
        uic.loadUi("Login.ui",self.logout_screen)
        self.logout_screen.show()
        self.logout_screen.SignUpButton.clicked.connect(self.load_signup_screen) #after the signup button has been clicked

    def load_signup_screen(self): #loading the sugnup screens
        self.SignUpScreen=QtWidgets.QMainWindow()
        uic.loadUi("SignUp.ui",self.SignUpScreen)
        self.SignUpScreen.show()


    def load_MyContent_screen(self): #loading the fan content screen
        self.MyContentScreen=QtWidgets.QMainWindow()
        uic.loadUi("My Content.ui",self.MyContentScreen)
        self.MyContentScreen.show()

    def load_Comments_and_details(self):
        self.comments_and_details_screen=QtWidgets.QMainWindow()
        uic.loadUi("Comments.ui",self.comments_and_details_screen)
        self.comments_and_details_screen.show()










app=QtWidgets.QApplication(sys.argv) #create an instance of QTwidgets.Qapplication
window=UI() #create an instance of our class
app.exec()