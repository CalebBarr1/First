import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Alpha028!",
  database="BankingInfo"
)

mycursor = mydb.cursor()

# Get all table names
mycursor.execute("SHOW TABLES")
tables = mycursor.fetchall()

# Loop through all tables and truncate them
for table in tables:
    tablename = table[0]
    mycursor.execute(f"TRUNCATE TABLE {tablename}")

print("All data cleared from all tables.")
