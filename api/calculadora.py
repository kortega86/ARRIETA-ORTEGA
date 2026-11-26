import html
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs


# PRODUCTOS Y PRECIOS POR METRO CUADRADO
PRODUCTOS = {
    "1": ("Ventana corrediza", 380000),
    "2": ("Puerta", 520000),
    "3": ("Puerta ventana", 450000),
    "4": ("Cerramiento", 420000),
    "5": ("Ventana proyectante", 480000),
}

# TIPOS DE VIDRIO
VIDRIOS = {
    "1": ("Vidrio claro", 1.0),
    "2": ("Vidrio templado (+25%)", 1.25),
}

# CÓDIGOS DE DESCUENTO
CODIGOS = {
    "ALUMINIO10": 0.10
}

# MEDIDA MÍNIMA PERMITIDA EN METROS
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
            mensaje = (
                f"Código {codigo} aplicado: "
                f"{int(CODIGOS[codigo] * 100)}% de descuento."
            )
        else:
            mensaje = "El código no es válido. Se muestra el valor sin descuento."

    return area_total, total, mensaje


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        contenido = """
        <h2>Calculadora de Arrieta Ortega</h2>
        <p>Para realizar una cotización, regresa al sitio y completa el formulario.</p>
        <a href="/">Volver al sitio</a>
        """
        self.enviar_pagina(contenido)

    def do_POST(self):

        longitud = int(self.headers.get("Content-Length", 0))
        datos = self.rfile.read(longitud).decode("utf-8")
        formulario = parse_qs(datos)

        try:
            # RECIBIR LOS DATOS DEL FORMULARIO
            producto_id = formulario.get("producto", [""])[0]
            ancho_texto = formulario.get("ancho", [""])[0]
            alto_texto = formulario.get("alto", [""])[0]
            vidrio_id = formulario.get("vidrio", [""])[0]
            cantidad_texto = formulario.get("cantidad", [""])[0]
            codigo = formulario.get("descuento", [""])[0]

            # VALIDAR EL PRODUCTO
            if producto_id not in PRODUCTOS:
                raise ValueError("Selecciona un producto válido.")

            nombre_producto, precio_m2 = PRODUCTOS[producto_id]

            # VALIDAR EL TIPO DE VIDRIO
            if vidrio_id not in VIDRIOS:
                raise ValueError("Selecciona un tipo de vidrio válido.")

            nombre_vidrio, factor_vidrio = VIDRIOS[vidrio_id]

            # CONVERTIR LAS MEDIDAS
            try:
                ancho = float(ancho_texto.replace(",", "."))
                alto = float(alto_texto.replace(",", "."))
            except ValueError:
                raise ValueError("Escribe valores numéricos válidos para el ancho y el alto.")

            # VALIDAR LAS MEDIDAS MÍNIMAS
            if ancho < MEDIDA_MINIMA or alto < MEDIDA_MINIMA:
                raise ValueError("El ancho y el alto deben ser como mínimo de 0.3 metros.")

            # VALIDAR LA CANTIDAD
            try:
                cantidad = int(cantidad_texto)
            except ValueError:
                raise ValueError("La cantidad debe ser un número entero.")

            if cantidad < 1:
                raise ValueError("La cantidad debe ser como mínimo 1.")

            # CALCULAR EL PEDIDO
            area, total, mensaje = calcular_pedido(
                precio_m2,
                ancho,
                alto,
                factor_vidrio,
                cantidad,
                codigo
            )

            # PREPARAR EL RESULTADO
            contenido = f"""
            <h2>Resumen de tu pedido</h2>

            <div class="dato">
                <span>Producto:</span>
                <strong>{html.escape(nombre_producto)}</strong>
            </div>

            <div class="dato">
                <span>Precio por m²:</span>
                <strong>{formatear_pesos(precio_m2)}</strong>
            </div>

            <div class="dato">
                <span>Ancho:</span>
                <strong>{ancho:.2f} m</strong>
            </div>

            <div class="dato">
                <span>Alto:</span>
                <strong>{alto:.2f} m</strong>
            </div>

            <div class="dato">
                <span>Tipo de vidrio:</span>
                <strong>{html.escape(nombre_vidrio)}</strong>
            </div>

            <div class="dato">
                <span>Cantidad:</span>
                <strong>{cantidad}</strong>
            </div>

            <div class="dato">
                <span>Área total:</span>
                <strong>{area:.2f} m²</strong>
            </div>

            <hr>

            <div class="dato total">
                <span>Valor total estimado:</span>
                <strong>{formatear_pesos(total)}</strong>
            </div>

            <p class="mensaje">{html.escape(mensaje)}</p>

            <p>
                Este valor es una estimación. La cotización definitiva
                se confirma después de verificar las medidas en obra.
            </p>

            <a class="boton" href="/#calculadora">Realizar otra cotización</a>
            <a class="boton secundario" href="/">Volver al inicio</a>
            """

        except ValueError as error:

            contenido = f"""
            <h2>No fue posible calcular tu pedido</h2>

            <p class="error">{html.escape(str(error))}</p>

            <p>Verifica la información e intenta nuevamente.</p>

            <a class="boton" href="/#calculadora">Regresar a la calculadora</a>
            """

        self.enviar_pagina(contenido)

    def enviar_pagina(self, contenido):

        pagina = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">

            <title>Resultado de cotización | Arrieta Ortega</title>

            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600&family=Barlow+Semi+Condensed:wght@600;700&display=swap" rel="stylesheet">

            <style>
                * {{
                    box-sizing: border-box;
                }}

                body {{
                    margin: 0;
                    padding: 30px 15px;
                    font-family: 'Barlow', sans-serif;
                    background: #f2f4f6;
                    color: #263238;
                }}

                .contenedor {{
                    max-width: 650px;
                    margin: 40px auto;
                    padding: 35px;
                    background: white;
                    border-radius: 14px;
                    box-shadow: 0 5px 25px rgba(0,0,0,0.08);
                }}

                h2 {{
                    font-family: 'Barlow Semi Condensed', sans-serif;
                    font-size: 30px;
                    margin-top: 0;
                    color: #263f50;
                }}

                .dato {{
                    display: flex;
                    justify-content: space-between;
                    gap: 15px;
                    padding: 12px 0;
                    border-bottom: 1px solid #e5e8eb;
                }}

                .dato strong {{
                    text-align: right;
                }}

                .total {{
                    font-size: 20px;
                    color: #263f50;
                    border-bottom: none;
                }}

                .mensaje {{
                    margin-top: 20px;
                    padding: 15px;
                    background: #eef4f6;
                    border-radius: 8px;
                }}

                .error {{
                    padding: 15px;
                    background: #fff0f0;
                    color: #a32626;
                    border-radius: 8px;
                }}

                .boton {{
                    display: inline-block;
                    margin-top: 15px;
                    margin-right: 8px;
                    padding: 12px 20px;
                    background: #263f50;
                    color: white;
                    text-decoration: none;
                    border-radius: 6px;
                    font-weight: 600;
                }}

                .secundario {{
                    background: #657984;
                }}

                @media (max-width: 480px) {{
                    .contenedor {{
                        padding: 22px;
                    }}

                    .dato {{
                        flex-direction: column;
                        gap: 5px;
                    }}

                    .dato strong {{
                        text-align: left;
                    }}
                }}
            </style>
        </head>

        <body>
            <main class="contenedor">
                {contenido}
            </main>
        </body>
        </html>
        """

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(pagina.encode("utf-8"))