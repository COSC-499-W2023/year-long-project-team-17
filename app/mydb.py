import mysql.connector

dataBase = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Dvy!2#4%cnbyy",
    auth_plugin="mysql_native_password",

)

#Prepare cursor object
cursorObject = dataBase.cursor()

#create database
cursorObject.execute("CREATE DATABASE elderco")

print("All done!")
