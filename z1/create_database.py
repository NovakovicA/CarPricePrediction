import mysql.connector

connection = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password"
)
connection.autocommit = True
cursor = connection.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS PSZ")
cursor.close()
connection.close()


connection = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="PSZ",
  charset="utf8"
)
connection.autocommit = True
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS Automobili(idOglasa VARCHAR(50) PRIMARY KEY, cena INT, stanje VARCHAR(30), marka VARCHAR(30), model VARCHAR(30), godiste INT, kilometraza INT, karoserija VARCHAR(30), gorivo VARCHAR(30), kubikaza INT, snagaMotora INT, menjac VARCHAR(30), brojVrata INT, boja VARCHAR(30), lokacijaProdavca VARCHAR(100))")
cursor.close()
connection.close()