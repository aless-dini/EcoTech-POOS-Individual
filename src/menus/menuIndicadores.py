from servicios.api_cmf import INDICADORES
from servicios.indicadores import ORIGEN_API, ORIGEN_BD, consultar_indicador, obtener_historial

def elegir_indicador():
    # Solo se ofrecen los indicadores admitidos; Enter vuelve sin consultar.
    codigos = list(INDICADORES)
    print("\nIndicadores disponibles:")
    for numero, codigo in enumerate(codigos, start=1):
        print(f"{numero}. {INDICADORES[codigo][0]}")
    while True:
        valor = input("Elija un indicador (Enter para volver): ").strip()
        if valor == "":
            return None
        if valor.isdigit() and 1 <= int(valor) <= len(codigos):
            return codigos[int(valor) - 1]
        if valor.lower() in INDICADORES:
            return valor.lower()
        print("Opción no válida, intente de nuevo.")

def formato_pesos(valor, decimales=2):
    # 39.485,65 al estilo chileno.
    return f"{valor:,.{decimales}f}".replace(",", "_").replace(".", ",").replace("_", ".")

def mostrar_verificacion(dato):
    if dato.verificado_en is None:
        return "sin registro"
    return dato.verificado_en.replace("T", " ")

def mostrar_origen(dato, origen):
    if origen == ORIGEN_API:
        print(f"Origen: {ORIGEN_API} ({dato.fuente})")
    else:
        print(f"Origen: {ORIGEN_BD}")
        print(f"Última verificación: {mostrar_verificacion(dato)}")

def consultar_valor_actualizado(usuario_actual):
    codigo = elegir_indicador()
    if codigo is None:
        return

    print("\nConsultando la API...")
    dato, origen, mensaje = consultar_indicador(usuario_actual, codigo)
    if dato is None:
        print(f"\n{mensaje}")
        return

    print(f"\n{INDICADORES[dato.codigo][0]}: ${formato_pesos(dato.valor)} ({dato.unidad})")
    print(f"Fecha del dato: {dato.fecha}")
    mostrar_origen(dato, origen)
    print(mensaje)

def ver_historial_guardado(usuario_actual):
    codigo = elegir_indicador()
    if codigo is None:
        return

    historial = obtener_historial(usuario_actual, codigo)
    if not historial:
        print(f"\nAún no existe historial de {INDICADORES[codigo][0]}.")
        return

    print(f"\nHistorial de {INDICADORES[codigo][0]} (del más reciente al más antiguo) · Origen: {ORIGEN_BD}")
    print(f"{'Fecha del dato':<16}{'Valor (' + historial[0].unidad + ')':>20}   Última verificación")
    for dato in historial:
        print(f"{dato.fecha:<16}{formato_pesos(dato.valor):>20}   {mostrar_verificacion(dato)}")
