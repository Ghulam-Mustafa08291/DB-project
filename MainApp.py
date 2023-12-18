from PyQt6 import QtWidgets, uic,QtGui, QtCore
import sys
import pyodbc
from PyQt6.QtWidgets import QTableWidgetItem,QMessageBox

#connecting the database below
server="LAPTOP-4OMLOR40"
database="AnimeDatabase"
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
        self.AccountCredentialchangescreen=None
        self.Login_Button.clicked.connect(self.after_logging_in)
        self.SignUpButton.clicked.connect(self.load_signup_screen)
        self.Anime_name="" #for storing the anime name being enterd in the home screen
       
        
        
        
        

    def after_logging_in(self): #to load the ui when we press the login Button, will show the home menu
        entered_username=self.lineEdit.text()
        entered_password=self.lineEdit_2.text()
        cursor.execute(f"SELECT Username FROM Users WHERE Username = '{entered_username}' AND U_password = '{entered_password}'")    
        rows=cursor.fetchall()
        if len(rows)==0:
            msg_box = QMessageBox()
            msg_box.setWindowTitle('Login failed')
            msg_box.setText('no user found!')
            msg_box.exec()
        else:
          
            print(rows)
            self.home_screen=QtWidgets.QMainWindow() #window is initialized to none in the init function
            uic.loadUi("HOME.ui",self.home_screen)
            self.home_screen.show()
            self.home_screen.pushButton_5.clicked.connect(self.after_clicking_updates) #when the updates button is clicked on the screen'
            self.home_screen.pushButton.clicked.connect(self.search_by_name) #when the search button is clicked on the home screen
            self.home_screen.pushButton_3.clicked.connect(self.show_login_screen)
            self.home_screen.pushButton_6.clicked.connect(self.load_MyContent_screen)
            self.home_screen.pushButton_7.clicked.connect(self.load_change_credential_screen) #for changing the account settings
            self.home_screen.pushButton_8.clicked.connect(self.load_Comments_and_details)
            # self.home_screen.tableWidget.itemSelectionChanged.connect(self.on_item_selected)
            self.home_screen.pushButton_8.clicked.connect(self.on_item_selected)

        





        
        
            


    def after_clicking_updates(self): # shows the updates screen
        self.update_screen=QtWidgets.QMainWindow()
        uic.loadUi("Updates.ui",self.update_screen)
        self.update_screen.show()
        self.update_screen.pushButton_3.clicked.connect(self.show_login_screen)
        self.update_screen.pushButton_6.clicked.connect(self.load_MyContent_screen)
        self.update_screen.pushButton_7.clicked.connect(self.load_change_credential_screen)
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
        self.SignUpScreen.pushButton_3.clicked.connect(self.signup_register) #when the register button is clicked
        


   
    def load_change_credential_screen(self):
        self.AccountCredentialchangescreen=QtWidgets.QMainWindow()
        uic.loadUi("AccountSettings.ui",self.AccountCredentialchangescreen)
        self.AccountCredentialchangescreen.show()
        self.AccountCredentialchangescreen.pushButton.clicked.connect(self.change_password)
        self.AccountCredentialchangescreen.pushButton_2.clicked.connect(self.Change_username)

    def change_password(self):
        current_password=self.lineEdit_2.text()
        entered_current_password=self.AccountCredentialchangescreen.lineEdit.text()
        entered_new_password=self.AccountCredentialchangescreen.lineEdit_2.text()

        if entered_current_password!=current_password:
            msg_box = QMessageBox()
            msg_box.setWindowTitle('ERROR')
            msg_box.setText('Password does not match with your current password!!')
            msg_box.exec()

        else:
            cursor.execute(f''' update Users set U_Password='{entered_new_password}'
                           where U_Password='{entered_current_password}'  ''')
            msg_box = QMessageBox()
            msg_box.setWindowTitle('DONE!')
            msg_box.setText('Password changed successfully!')
            msg_box.exec()
            connection.commit()



    def Change_username(self):
        current_username=self.lineEdit.text()
        entered_current_username=self.AccountCredentialchangescreen.lineEdit_4.text()
        entered_new_username=self.AccountCredentialchangescreen.lineEdit_3.text()

        if entered_current_username!=current_username:
            msg_box = QMessageBox()
            msg_box.setWindowTitle('ERROR')
            msg_box.setText('Username does not match with your current username!')
            msg_box.exec()

        else:
            cursor.execute(f''' update Users set Username='{entered_new_username}'
                           where Username='{entered_current_username}'  ''')
            msg_box = QMessageBox()
            msg_box.setWindowTitle('DONE!')
            msg_box.setText('Username changed successfully!')
            msg_box.exec()
            connection.commit()

        print("your really wanto to change the current username: ",current_username," ?")
       # entered_password=self.lineEdit_2.text()


    def signup_register(self):
        username=self.SignUpScreen.lineEdit.text()
        password=self.SignUpScreen.lineEdit_2.text()
        access_level=self.SignUpScreen.lineEdit_3.text()
        max_user_id_query = cursor.execute('SELECT MAX(UserID) FROM Users') #will later add 1 to it for assigning new Id everytime
        max_user_id = max_user_id_query.fetchone()[0]  # Get the maximum UserID

    # Increment the UserID for the new user
        if max_user_id is not None:
            user_id = max_user_id + 1  # Increment the maximum UserID by 1 for the new user
        else:
            user_id = 1  # If no users exist, start from 1
        cursor.execute('INSERT INTO Users (UserID, Username, U_Password, AccessLevel) VALUES (?,?, ?,?)', (user_id,username, password,access_level))
        connection.commit()


        msg_box = QMessageBox()
        msg_box.setWindowTitle('Confirmation')
        msg_box.setText('User added!')
        msg_box.exec()
        #print("user added!")

    def add_comment_to_both(self):
        
        anime_id=self.comments_and_details_screen.lineEdit_2.text()
        comment=self.comments_and_details_screen.textEdit.toPlainText()
        manga_id=self.comments_and_details_screen.lineEdit_4.text()
        series_name=self.comments_and_details_screen.lineEdit.text()
        series_id=cursor.execute(f'''  select SeriesID from Series where SeriesName = '{series_name}' ''')
        series_id=series_id.fetchone()[0]
        entered_username=self.lineEdit.text()
        user_id=cursor.execute(f'''select UserID from Users where Username= '{entered_username}' ''')
        user_id=user_id.fetchone()[0]
        print ("the series name: ",series_name, " and the series id is: ",series_id)
        print(comment)
        cursor.execute("SELECT MAX(CommentID) FROM Comments")
        comment_id_result = cursor.fetchone()
        if comment_id_result[0] is not None:
            comment_id = comment_id_result[0] + 1
        else:
            comment_id = 1
        # comment_id=cursor.execute("select max(CommentID) from Comments")
        # comment_id=comment_id.fetchone()[0]
        # comment_id+=1
        print("new comment id is: ",comment_id)
        print("userid is: ",user_id)
        print("manga id is: ",manga_id)
        cursor.execute(f''' INSERT INTO Comments(CommentID,UserId,ReplytoID,CommentText) VALUES (?,?,NULL,?)''',(comment_id,user_id,comment))
        connection.commit()        
        cursor.execute(f''' INSERT INTO MangaComment(CommentID,MangaID,SeriesID) VALUES(?,?,?)''',(comment_id,manga_id,series_id))
        connection.commit()
        cursor.execute(f''' INSERT INTO AnimeComment(CommentID,AnimeID,SeriesID,SeasonNo) VALUES(?,?,?,?)''',(comment_id,anime_id,series_id,1))

        connection.commit()

    def load_MyContent_screen(self): #loading the fan content screen
        self.MyContentScreen=QtWidgets.QMainWindow()
        uic.loadUi("My Content.ui",self.MyContentScreen)
        self.MyContentScreen.show()

    def load_Comments_and_details(self):
        self.comments_and_details_screen=QtWidgets.QMainWindow()
        uic.loadUi("Comments.ui",self.comments_and_details_screen)
        self.comments_and_details_screen.show()
        self.comments_and_details_screen.pushButton.clicked.connect(self.add_comment_to_anime)
        self.comments_and_details_screen.pushButton_2.clicked.connect(self.add_comment_to_manga)
        self.comments_and_details_screen.pushButton_3.clicked.connect(self.add_comment_to_both)

    def add_comment_to_manga(self):
        comment=self.comments_and_details_screen.textEdit.toPlainText()
        manga_id=self.comments_and_details_screen.lineEdit_4.text()
        series_name=self.comments_and_details_screen.lineEdit.text()
        series_id=cursor.execute(f'''  select SeriesID from Series where SeriesName = '{series_name}' ''')
        series_id=series_id.fetchone()[0]
        entered_username=self.lineEdit.text()
        user_id=cursor.execute(f'''select UserID from Users where Username= '{entered_username}' ''')
        user_id=user_id.fetchone()[0]
        print ("the series name: ",series_name, " and the series id is: ",series_id)
        print(comment)
        cursor.execute("SELECT MAX(CommentID) FROM Comments")
        comment_id_result = cursor.fetchone()
        if comment_id_result[0] is not None:
            comment_id = comment_id_result[0] + 1
        else:
            comment_id = 1
        # comment_id=cursor.execute("select max(CommentID) from Comments")
        # comment_id=comment_id.fetchone()[0]
        # comment_id+=1
        print("new comment id is: ",comment_id)
        print("userid is: ",user_id)
        print("manga id is: ",manga_id)
        cursor.execute(f''' INSERT INTO Comments(CommentID,UserId,ReplytoID,CommentText) VALUES (?,?,NULL,?)''',(comment_id,user_id,comment))
        connection.commit()        
        cursor.execute(f''' INSERT INTO MangaComment(CommentID,MangaID,SeriesID) VALUES(?,?,?)''',(comment_id,manga_id,series_id))
        
        connection.commit()


    def add_comment_to_anime(self):
        comment=self.comments_and_details_screen.textEdit.toPlainText()
        anime_id=self.comments_and_details_screen.lineEdit_2.text()
        series_name=self.comments_and_details_screen.lineEdit.text()
        series_id=cursor.execute(f'''  select SeriesID from Series where SeriesName = '{series_name}' ''')
        series_id=series_id.fetchone()[0]
        entered_username=self.lineEdit.text()
        user_id=cursor.execute(f'''select UserID from Users where Username= '{entered_username}' ''')
        user_id=user_id.fetchone()[0]
        print ("the series name: ",series_name, " and the series id is: ",series_id)
        print(comment)
        cursor.execute("SELECT MAX(CommentID) FROM Comments")
        comment_id_result = cursor.fetchone()
        if comment_id_result[0] is not None:
            comment_id = comment_id_result[0] + 1
        else:
            comment_id = 1
        # comment_id=cursor.execute("select max(CommentID) from Comments")
        # comment_id=comment_id.fetchone()[0]
        # comment_id+=1
        print("new comment id is: ",comment_id)
        print("userid is: ",user_id)
        print("anime id is: ",anime_id)
        cursor.execute(f''' INSERT INTO Comments(CommentID,UserId,ReplytoID,CommentText) VALUES (?,?,NULL,?)''',(comment_id,user_id,comment))
        connection.commit()        
        cursor.execute(f''' INSERT INTO AnimeComment(CommentID,AnimeID,SeriesID,SeasonNo) VALUES(?,?,?,?)''',(comment_id,anime_id,series_id,1))
        
        connection.commit()



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
            commentstuff=cursor.execute(f''' SELECT * FROM Comments WHERE CommentID IN (select CommentID from AnimeComment where AnimeID='{anime_id}') ''').fetchall()
            print(commentstuff)
            for i in range(len(commentstuff)):
                for j in range(len(commentstuff[i])):
                    item=QTableWidgetItem(str(commentstuff[i][j]))
                    print(i,j,item.text())
                    self.comments_and_details_screen.tableWidget.setItem(i,j,item)









app=QtWidgets.QApplication(sys.argv) #create an instance of QTwidgets.Qapplication
window=UI() #create an instance of our class
app.exec()