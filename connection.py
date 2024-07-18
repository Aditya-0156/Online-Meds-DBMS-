
import mysql.connector
# create a connection to the database
db = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="OnlineMeds")
# create a cursor
cursor = db.cursor()