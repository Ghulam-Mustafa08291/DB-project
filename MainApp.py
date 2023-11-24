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
        self.Anime_name="" #for storing the anime name being enterd in the home screen
        
        
        
        

    def after_logging_in(self): #to load the ui when we press the login Button, will show the home menu
        self.home_screen=QtWidgets.QMainWindow() #window is initialized to none in the init function
        uic.loadUi("HOME.ui",self.home_screen)
        self.home_screen.show()
        self.home_screen.pushButton_5.clicked.connect(self.after_clicking_updates) #when the updates button is clicked on the screen'
        self.home_screen.pushButton.clicked.connect(self.search_by_name) #when the search button is clicked on the home screen
        self.home_screen.pushButton_3.clicked.connect(self.show_login_screen)
        self.home_screen.pushButton_6.clicked.connect(self.load_MyContent_screen)
        self.home_screen.pushButton_8.clicked.connect(self.load_Comments_and_details)
        # self.home_screen.tableWidget.itemSelectionChanged.connect(self.on_item_selected)
        self.home_screen.pushButton_8.clicked.connect(self.on_item_selected)
        
            


    def after_clicking_updates(self): # shows the updates screen
        self.update_screen=QtWidgets.QMainWindow()
        uic.loadUi("Updates.ui",self.update_screen)
        self.update_screen.show()
        self.update_screen.pushButton_3.clicked.connect(self.show_login_screen)
        self.update_screen.pushButton_6.clicked.connect(self.load_MyContent_screen)
        self.update_screen.pushButton_8.clicked.connect(self.after_logging_in)

    def search_by_name(self): #for searching through the name in the HOME screen ui
        self.Anime_name=self.home_screen.lineEdit.text()

        cursor.execute( f'''
        SELECT S.SeriesName, A.AnimeID, M.MangaID, A.EndDate
        FROM Anime A
        JOIN Series S ON A.SeriesID = S.SeriesID
        LEFT JOIN Manga M ON A.SeriesID = M.SeriesID
        WHERE A.EndDate IS NOT NULL
        AND S.SeriesName = '{self.Anime_name}'
''')
        rows=cursor.fetchall()
        for row in range(len(rows)):
            for j in range(len(rows[row])):
                item=QTableWidgetItem(str(rows[row][j]))
                self.home_screen.tableWidget.setItem(row,j,item)
               # print(row)
           
       
            

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

    def on_item_selected(self):
        # Get the selected item(s)
        selected_items = self.home_screen.tableWidget.selectedItems()

        # Assuming the table has multiple columns, capturing the data based on the column index
        if selected_items:
            selected_row = []
            for item in selected_items:
                selected_row.append(item.text())  # Get the text of the selected item
            #print(selected_items)
            series_name = selected_row[0]  
            anime_id = selected_row[1] 
            manga_id = selected_row[2] 
            publisher_id=cursor.execute(f'''  select PublisherID from Manga where MangaId='{manga_id}' ''').fetchone()
            print(f"Selected SeriesName: {series_name}, AnimeID: {anime_id}, MangaID: {manga_id}, PublisherID: {publisher_id[0]}")
            self.comments_and_details_screen.lineEdit.setText(series_name)
            self.comments_and_details_screen.lineEdit_2.setText(anime_id)
            self.comments_and_details_screen.lineEdit_3.setText(str(publisher_id[0]))
            self.comments_and_details_screen.lineEdit_4.setText(manga_id)

            commentstuff=cursor.execute(f''' select * from Comments where AnimeID='{anime_id}' ''').fetchall()
            for i in commentstuff:
                print(i[0])










app=QtWidgets.QApplication(sys.argv) #create an instance of QTwidgets.Qapplication
window=UI() #create an instance of our class
app.exec()