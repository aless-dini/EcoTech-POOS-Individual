def pedir_dato(mensaje, validador, leer=input):
    while True:
        try:
            return validador(leer(mensaje))
        except (TypeError, ValueError) as error:
            print(f"{error} Intenta nuevamente.")

def pedir_opcional(mensaje, validador):
    # Enter deja el valor como estaba (devuelve None).
    while True:
        valor = input(mensaje).strip()
        if not valor:
            return None
        try:
            return validador(valor)
        except (TypeError, ValueError) as error:
            print(f"{error} Intenta nuevamente.")
