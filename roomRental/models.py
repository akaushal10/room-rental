import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="abhishek",
  password="Abhi@123",
  database="room_rental"
)

cursor = db.cursor()