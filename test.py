import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Alpha028!",
  database="BankingInfo"
)
mycursor = mydb.cursor()



print(mycursor.execute("SHOW TABLES"))
print(mycursor.fetchall())

print(mycursor.execute("SHOW CREATE TABLE accounts"))

print(mycursor.fetchall())