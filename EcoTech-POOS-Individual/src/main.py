import sqlite3
import pymysql
from persistencia.crear_bd import crear_tablas
from menus.menuPrincipal import menu_principal

def main():
    try:
        crear_tablas()
    except (sqlite3.Error, pymysql.MySQLError, ValueError) as e:
        print(f"No fue posible conectarse a la base de datos: {e}")
        print("Revise la configuración del archivo .env e intente de nuevo.")
        return

    print("Base de datos preparada correctamente.")
    try:
        menu_principal()
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma cerrado.")

if __name__ == "__main__":
    main()
