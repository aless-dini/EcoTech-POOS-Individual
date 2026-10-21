import os
import sqlite3
import pymysql
from pymysql.constants import CLIENT
from dotenv import load_dotenv

load_dotenv()

def obtener_motor():
    return os.getenv("DB_ENGINE", "sqlite").lower()

def abrir_conexion():
    motor = obtener_motor()

    if motor == "sqlite":
        conexion = sqlite3.connect(os.getenv("DB_NAME", "ecotech.db"))
        conexion.execute("PRAGMA foreign_keys = ON")
        return conexion

    if motor == "mysql":
        return pymysql.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            charset="utf8mb4",
            client_flag=CLIENT.FOUND_ROWS,
            sql_mode="STRICT_ALL_TABLES",
        )
    
    raise ValueError(f"Motor no soportado: {motor}")

def marcador_sql():
    if obtener_motor() == "sqlite":
        return "?"
    return "%s"
