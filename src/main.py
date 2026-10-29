import logging
from persistencia.crear_bd import crear_tablas
from persistencia.errores import ErrorBaseDatos
from persistencia.semilla_bd import cargar_cuenta_admin
from menus.menuPrincipal import menu_principal
from menus.menuUsuario import solicitar_login

ARCHIVO_LOG = "ecotech.log"

def configurar_log():
    # Los detalles técnicos de los errores quedan en el archivo, no en pantalla.
    logging.basicConfig(filename=ARCHIVO_LOG, encoding="utf-8", level=logging.WARNING,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")

def main():
    configurar_log()
    try:
        crear_tablas()
        cargar_cuenta_admin()
    except ErrorBaseDatos as e:
        print(e)
        print(f"Revise la configuración del archivo .env (detalle técnico en {ARCHIVO_LOG}).")
        return

    print("Base de datos preparada correctamente.")
    print("\n*****Bienvenido al programa de Ecotech*****")
    try:
        while True:
            try:
                usuario_actual = solicitar_login()
            except ErrorBaseDatos as e:
                print(f"\n{e}")
                usuario_actual = None
            if usuario_actual is None:
                if input("Enter para reintentar o 0 para salir: ").strip() == "0":
                    break
                continue
            opcion = menu_principal(usuario_actual)
            usuario_actual = None
            if opcion == "salir":
                break
            print("\nSesión cerrada. Ingrese nuevamente.")
        print("Hasta luego!")
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma cerrado.")

if __name__ == "__main__":
    main()
