import mysql.connector

def conecta():
    return mysql.connector.connect(
                host="localhost",
                user="root",
                password="password",
                database="centroexplicacoes2"
            )