# calculadora.py
# Lógica de la calculadora de Arrieta Ortega Ingeniería de Proyectos.
# Usa los mismos productos, precios y códigos que la sección #calculadora del index.html.

PRODUCTOS = {
    "1": ("Ventana corrediza", 380000),
    "2": ("Puerta", 520000),
    "3": ("Puerta ventana", 450000),
    "4": ("Cerramiento", 420000),
    "5": ("Ventana proyectante", 480000),
}

VIDRIOS = {
    "1": ("Vidrio claro", 1.0),
    "2": ("Vidrio templado (+25%)", 1.25),
}

CODIGOS = {"ALUMINIO10": 0.10}

MEDIDA_MINIMA = 0.3


def formatear_pesos(valor):
    return "$" + f"{valor:,.0f}".replace(",", ".")


def calcular_pedido(precio_m2, ancho, alto, factor_vidrio, cantidad, codigo=""):
    area_total = ancho * alto * cantidad
    total = area_total * precio_m2 * factor_vidrio
    mensaje = "Valor estimado. La cotización final se confirma con las medidas en obra."

    codigo = codigo.strip().upper()
    if codigo:
        if codigo in CODIGOS:
            total = total * (1 - CODIGOS[codigo])
            mensaje = f"Código {codigo} aplicado: {int(CODIGOS[codigo] * 100)}% de descuento."
        else:
            mensaje = "El código no es válido. Se muestra el valor sin descuento."

    return area_total, total, mensaje


def pedir_opcion(texto, opciones):
    while True:
        eleccion = input(texto).strip()
        if eleccion in opciones:
            return opciones[eleccion]
        print("Opción no válida. Intenta de nuevo.")


def pedir_numero(texto, minimo):
    while True:
        try:
            valor = float(input(texto).replace(",", "."))
        except ValueError:
            print("Escribe un número, por ejemplo 1.5")
            continue
        if valor < minimo:
            print(f"El valor mínimo es {minimo}.")
            continue
        return valor


def main():
    print("=== Calculadora de pedido - Arrieta Ortega ===")
    print("Productos:")
    for clave, (nombre, precio) in PRODUCTOS.items():
        print(f"  {clave}. {nombre} - {formatear_pesos(precio)} por m²")

    nombre_producto, precio_m2 = pedir_opcion("Elige un producto (1-5): ", PRODUCTOS)
    ancho = pedir_numero("Ancho en metros: ", MEDIDA_MINIMA)
    alto = pedir_numero("Alto en metros: ", MEDIDA_MINIMA)

    print("Tipo de vidrio:")
    for clave, (nombre, _) in VIDRIOS.items():
        print(f"  {clave}. {nombre}")
    nombre_vidrio, factor_vidrio = pedir_opcion("Elige el vidrio (1-2): ", VIDRIOS)

    cantidad = int(pedir_numero("Cantidad: ", 1))
    codigo = input("Código de descuento (Enter si no tienes): ")

    area, total, mensaje = calcular_pedido(precio_m2, ancho, alto, factor_vidrio, cantidad, codigo)

    print("\n--- Resumen de tu pedido ---")
    print(f"Producto: {nombre_producto} x {cantidad}")
    print(f"Vidrio: {nombre_vidrio}")
    print(f"Área total: {area:.2f} m²")
    print(f"Valor total: {formatear_pesos(total)}")
    print(mensaje)


if __name__ == "__main__":
    main()
