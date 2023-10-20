import mysql.connector

dataBase = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    auth_plugin="mysql_native_password",

)

#Prepare cursor object
cursorObject = dataBase.cursor()

#create database
cursorObject.execute("CREATE DATABASE elderco")

print("All done!")
