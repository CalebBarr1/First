import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Alpha028!",
  database="BankingInfo"
)

mycursor = mydb.cursor()

def retrieve_all_data():
    mycursor.execute("SHOW TABLES")
    
    tables = [table[0] for table in mycursor.fetchall()]
    for table in tables:
        print("Table:", table)
        mycursor.execute(f"SELECT * FROM {table}")
        rows = mycursor.fetchall()
        for row in rows:
            print(row)

retrieve_all_data()
