import sqlite3
import pymysql
from persistencia.crear_bd import crear_tablas
from persistencia.semilla_bd import cargar_cuenta_admin
from menus.menuPrincipal import menu_principal
from menus.menuUsuario import solicitar_login

def main():
    try:
        crear_tablas()
        cargar_cuenta_admin()
    except (sqlite3.Error, pymysql.MySQLError, ValueError) as e:
        print(f"No fue posible conectarse a la base de datos: {e}")
        print("Revise la configuración del archivo .env e intente de nuevo.")
        return

    print("Base de datos preparada correctamente.")
    print("\n*****Bienvenido al programa de Ecotech*****")
    try:
        while True:
            usuario_actual = solicitar_login()
            if usuario_actual is None:
                if input("Enter para reintentar o 0 para salir: ").strip() == "0":
                    break
                continue
            opcion = menu_principal(usuario_actual)
            usuario_actual = None  # Terminar el acceso de esta sesión.
            if opcion == "salir":
                break
            print("\nSesión cerrada. Ingrese nuevamente.")
        print("Hasta luego!")
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma cerrado.")

if __name__ == "__main__":
    main()
