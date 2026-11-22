"""Menú interactivo por consola."""

from .entidades import Cliente
from .excepciones import DatosInvalidosError, ErrorSistema
from .pruebas import ejecutar_pruebas
from .registro import logger
from .servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala
from .sistema import SistemaSoftwareFJ


# ---- Utilidades de entrada: repiten la pregunta hasta recibir un dato válido ----
def pedir_texto(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("El campo no puede quedar vacío. Intente nuevamente.")


def pedir_entero(mensaje, minimo=1):
    while True:
        try:
            valor = int(input(mensaje))
        except ValueError:
            print("Entrada inválida. Ingrese un número entero.")
            continue
        if valor < minimo:
            print(f"Debe ingresar un número igual o mayor que {minimo}.")
            continue
        return valor


def pedir_decimal(mensaje, minimo=0.01, maximo=None):
    while True:
        try:
            valor = float(input(mensaje).replace(",", "."))
        except ValueError:
            print("Entrada inválida. Ingrese un número.")
            continue
        if valor < minimo or (maximo is not None and valor > maximo):
            limite = f" y máximo {maximo}" if maximo is not None else ""
            print(f"El valor debe ser mayor o igual a {minimo}{limite}.")
            continue
        return valor


def mostrar_menu():
    print("\n" + "=" * 62)
    print("       SOFTWARE FJ - SISTEMA DE GESTIÓN")
    print("=" * 62)
    for linea in ("1. Registrar cliente", "2. Registrar servicio", "3. Crear reserva",
                  "4. Confirmar reserva", "5. Procesar reserva", "6. Cancelar reserva",
                  "7. Consultar clientes", "8. Consultar servicios",
                  "9. Consultar reservas", "10. Ejecutar las 18 pruebas automáticas",
                  "0. Salir"):
        print(linea)
    print("=" * 62)


# ---- Opciones del menú ----
def registrar_cliente_menu(sistema):
    print("\n--- REGISTRO DE CLIENTE ---")
    cliente = Cliente(pedir_texto("Identificación del cliente: "),
                      pedir_texto("Nombre completo: "),
                      pedir_texto("Correo electrónico: "),
                      pedir_texto("Teléfono: "))
    sistema.registrar_cliente(cliente)
    print("Cliente registrado correctamente.")


def registrar_servicio_menu(sistema):
    print("\n--- REGISTRO DE SERVICIO ---")
    print("1. Reserva de sala\n2. Alquiler de equipos\n3. Asesoría especializada")
    tipo = input("Seleccione el tipo de servicio: ").strip()
    identificador = pedir_texto("Código del servicio: ")
    nombre = pedir_texto("Nombre del servicio: ")
    tarifa = pedir_decimal("Tarifa base: $", 0.01)

    if tipo == "1":
        servicio = ReservaSala(identificador, nombre, tarifa,
                               pedir_entero("Capacidad de la sala (personas): "))
    elif tipo == "2":
        servicio = AlquilerEquipo(identificador, nombre, tarifa,
                                  pedir_entero("Unidades disponibles (puede ser 0): ", 0))
    elif tipo == "3":
        servicio = AsesoriaEspecializada(identificador, nombre, tarifa,
                                         pedir_texto("Especialidad de la asesoría: "))
    else:
        raise DatosInvalidosError("Tipo de servicio no válido.")
    sistema.registrar_servicio(servicio)
    print("Servicio registrado correctamente.")


def crear_reserva_menu(sistema):
    print("\n--- CREAR RESERVA ---")
    if not sistema.clientes:
        print("Primero debe registrar al menos un cliente.")
        return
    if not sistema.servicios:
        print("Primero debe registrar al menos un servicio.")
        return

    print("\nClientes disponibles:")
    for cliente in sistema.clientes:
        print(f"  {cliente.identificador}: {cliente.nombre}")
    print("\nServicios disponibles:")
    for servicio in sistema.servicios:
        estado = "Disponible" if servicio.disponible else "No disponible"
        print(f"  {servicio.identificador}: {servicio.nombre} | {estado}")

    codigo = pedir_texto("Código de la reserva: ")
    id_cliente = pedir_texto("Código del cliente: ")
    id_servicio = pedir_texto("Código del servicio: ")
    duracion = pedir_decimal("Duración (horas o días según servicio): ", 0.01)

    # Se pregunta la cantidad solo si el servicio la requiere.
    servicio = sistema.buscar_servicio(id_servicio)
    cantidad = pedir_entero("Cantidad de equipos: ") if servicio.requiere_cantidad else 1

    reserva = sistema.crear_reserva(codigo, id_cliente, id_servicio, duracion, cantidad)
    print("Reserva creada correctamente.")
    print(reserva.mostrar_informacion())


def confirmar_reserva_menu(sistema):
    codigo = pedir_texto("Código de la reserva que desea confirmar: ")
    print(sistema.buscar_reserva(codigo).confirmar())


def procesar_reserva_menu(sistema):
    reserva = sistema.buscar_reserva(pedir_texto("Código de la reserva que desea procesar: "))
    descuento = pedir_decimal("Descuento (ejemplo 0.10 para 10%, 0 para ninguno): ", 0, 0.99)
    print(f"Reserva procesada. Total a pagar: ${reserva.procesar(descuento=descuento):,.2f}")


def cancelar_reserva_menu(sistema):
    print(sistema.buscar_reserva(pedir_texto("Código de la reserva que desea cancelar: ")).cancelar())


def _consultar(titulo, elementos, vacio):
    print(f"\n--- {titulo} ---")
    if not elementos:
        print(vacio)
    for elemento in elementos:
        print(elemento.mostrar_informacion())


def consultar_clientes(sistema):
    _consultar("CLIENTES REGISTRADOS", sistema.clientes, "No hay clientes registrados.")


def consultar_servicios(sistema):
    _consultar("SERVICIOS REGISTRADOS", sistema.servicios, "No hay servicios registrados.")


def consultar_reservas(sistema):
    _consultar("RESERVAS REGISTRADAS", sistema.reservas, "No hay reservas registradas.")


def ejecutar_menu_interactivo():
    """Bucle principal: ningún error del usuario cierra el programa."""
    sistema = SistemaSoftwareFJ()
    acciones = {
        "1": registrar_cliente_menu, "2": registrar_servicio_menu,
        "3": crear_reserva_menu, "4": confirmar_reserva_menu,
        "5": procesar_reserva_menu, "6": cancelar_reserva_menu,
        "7": consultar_clientes, "8": consultar_servicios, "9": consultar_reservas,
    }
    print("\nBienvenido al sistema Software FJ.")
    print("Los datos se mantienen en memoria mientras el programa está abierto.")
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "0":
            print("Gracias por utilizar Software FJ. ¡Hasta pronto!")
            logger.info("El usuario cerró el sistema desde el menú.")
            break
        if opcion == "10":
            ejecutar_pruebas()
            continue

        accion = acciones.get(opcion)
        if accion is None:
            print("Opción no válida. Seleccione una opción del menú.")
            continue

        try:
            accion(sistema)
        except ErrorSistema as error:
            print(f"\nNo se pudo completar la operación: {error}")
            logger.error("Error controlado desde el menú: %s", error)
        except (ValueError, TypeError) as error:
            print(f"\nDato incorrecto: {error}")
            logger.exception("Error de entrada desde el menú.")
        except Exception as error:
            print(f"\nOcurrió un error inesperado: {error}")
            logger.exception("Error inesperado desde el menú.")
        else:
            logger.info("Opción %s ejecutada correctamente.", opcion)
        finally:
            print("\nRegresando al menú principal...")
