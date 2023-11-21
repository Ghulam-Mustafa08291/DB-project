# keeping the code here commented for now
# import pyodbc

# server="LAPTOP-4OMLOR40"
# database="AnimeManagement"
# use_windows_authentication=True
# username=""
# password=""


# if use_windows_authentication:
#     connection_string=f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"
# else:
#    connection_string= f"Driver={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"



# connection=pyodbc.connect(connection_string)

# cursor=connection.cursor()
# cursor.execute("select * from Anime")

# rows=cursor.fetchall()

# for row in rows:
#     print(row)



















# # import pyodbc as odbccon
# # conn= odbccon.connect(" DRIVER ={ ODBC Driver 17 for SQL Server };"
# #                       "Server=LAPTOP-4OMLOR40;"
# #                       "Database=AnimeManagement;"
# #                       "Trusted_Connection=yes;")

# # cursor=conn.cursor()
# # cursor.execute("Select * from Anime")
# # for row in cursor:
# #     print("The anime id is: %r" %(row,))
# #     #print(row)