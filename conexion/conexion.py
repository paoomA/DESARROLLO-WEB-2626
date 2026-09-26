import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()


def obtener_conexion():

    # En Render usamos Aiven
    if os.getenv("MYSQL_HOST"):
        conexion = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            port=int(os.getenv("MYSQL_PORT", 3306)),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
            ssl_disabled=False
        )

    # En tu computadora seguimos usando MySQL Workbench
    else:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password=os.getenv("MYSQL_PASSWORD"),
            database="paoou_fashion"
        )

    return conexion