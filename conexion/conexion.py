import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()


def obtener_conexion():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("MYSQL_PASSWORD"),
        database="paoou_fashion"
    )

    return conexion