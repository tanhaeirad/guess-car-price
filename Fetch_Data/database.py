# This is for manage Database:

import mysql.connector  # for connect to mysql server

# configure your database here:
host = "localhost"
user = "root"
password = ""
database = "bama"
table = "data"


class DB:
    def __init__(self):

        # connect to database, create database, create table if is not exist
        try:
            self.my_db = mysql.connector.connect(
                host=host,
                user=user,
                passwd=password
            )
            self.my_cursor = self.my_db.cursor()

            self.create_database()
            self.create_table(table)

            self.my_cursor.close()

        except mysql.connector.Error as error:
            print("Something went wrong: {}".format(error))

    def create_database(self):
        self.my_cursor = self.my_db.cursor()

        self.my_cursor.execute("SHOW DATABASES")

        exist_databases = []
        for _database in self.my_cursor:
            exist_databases.append(_database[0])

        if database not in exist_databases:
            self.my_cursor = self.my_db.cursor()
            stm = "CREATE DATABASE " + database
            self.my_cursor.execute(stm)

        stm = "USE " + database
        self.my_cursor.execute(stm)
        self.my_cursor.close()

    def create_table(self, name):
        self.my_cursor = self.my_db.cursor()

        table = name
        self.my_cursor.execute("SHOW TABLES")
        exist_table = []
        for _table in self.my_cursor:
            exist_table.append(_table[0])

        if table not in exist_table:
            my_cursor = self.my_db.cursor()
            stm = "CREATE TABLE " + table + " (brand VARCHAR(255), model VARCHAR(255), kilometers VARCHAR(255), year VARCHAR(255), cost VARCHAR(255))"
            my_cursor.execute(stm)

    def insert_to_table(self, data):
        try:
            my_db = mysql.connector.connect(
                host=host,
                user=user,
                passwd=password
            )

            my_cursor = my_db.cursor()
            stm = "USE " + database
            my_cursor.execute(stm)
            my_cursor.close()

            my_cursor = my_db.cursor()
            sql = "INSERT INTO " + table + " (brand, model, kilometers, year, cost) VALUES (%s, %s, %s, %s, %s)"
            val = data
            my_cursor.execute(sql, val)
            my_db.commit()
            my_cursor.close()
            my_db.close()
        except mysql.connector.errors as error:
            print("Something went wrong: {}".format(error))

    def select(self, brand, model):
        try:
            my_db = mysql.connector.connect(
                host=host,
                user=user,
                passwd=password
            )
            my_cursor = my_db.cursor()
            stm = "USE " + database
            my_cursor.execute(stm)
            my_cursor.close()

            mycursor = my_db.cursor()

            mycursor.execute("SELECT * FROM " + table + " WHERE brand='" + brand + "' AND model='" + model + "'")

            myresult = mycursor.fetchall()

            return myresult

        except mysql.connector.errors as error:
            print("Something went wrong: {}".format(error))
