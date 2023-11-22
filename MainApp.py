from PyQt6 import QtWidgets, uic,QtGui, QtCore
import sys
import pyodbc

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
        self.Login_Button.clicked.connect(self.after_logging_in)
        

    def after_logging_in(self): #to load the ui when we press the login Button, will show the home menu
        self.home_screen=QtWidgets.QMainWindow() #window is initialized to none in the init function
        uic.loadUi("HOME.ui",self.home_screen)
        self.home_screen.show()
        self.home_screen.pushButton_5.clicked.connect(self.after_clicking_updates) #when the updates button is clicked on the screen'
        self.home_screen.pushButton.clicked.connect(self.search_by_name)
        self.home_screen.pushButton_3.clicked.connect(self.show_login_screen)
            


    def after_clicking_updates(self): # shows the updates screen
        self.update_screen=QtWidgets.QMainWindow()
        uic.loadUi("Updates.ui",self.update_screen)
        self.update_screen.show()
        self.update_screen.pushButton_3.clicked.connect(self.show_login_screen)

    def search_by_name(self): #for searching through the name in the HOME screen ui
        name=self.home_screen.lineEdit.text()
        #print(name)
        cursor.execute(f"select * from Series where SeriesName='{name}'")
        rows=cursor.fetchall()
        for row in rows:
            print(row)

    def show_login_screen(self):
        self.logout_screen=QtWidgets.QMainWindow() #window is initialized to none in the init function
        uic.loadUi("Login.ui",self.logout_screen)
        self.logout_screen.show()







app=QtWidgets.QApplication(sys.argv) #create an instance of QTwidgets.Qapplication
window=UI() #create an instance of our class
app.exec()